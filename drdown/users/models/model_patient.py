from django.apps import apps
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone
from drdown.notifications.utils import mail
from ..utils.validators import validate_ses
from ..utils.validators import validate_generic_number
from ..utils.validators import validate_names
from ..utils.validators import validate_sus

from celery.schedules import crontab
from celery.task import periodic_task

from .model_user import User, BaseUserSave, BaseUserDelete
from .model_responsible import Responsible


class Patient(BaseUserSave, BaseUserDelete, models.Model):
    user = models.OneToOneField(
        User,
        related_name='patient',
        on_delete=models.CASCADE,
        limit_choices_to=Q(has_specialization=False),
        verbose_name=_('User')
    )
    ses = models.CharField(
        help_text=_("Please, enter the valid SES number"),
        unique=True,
        max_length=9,
        validators=[validate_ses],
    )

    responsible = models.ForeignKey(
        Responsible,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Responsible')
    )

    mother_name = models.CharField(
        _('Name of mother'),
        help_text=_("Please, insert your mother name"),
        max_length=80,
        validators=[validate_names],
    )

    father_name = models.CharField(
        _('Name of father'),
        help_text=_("Please, insert your father name"),
        max_length=80,
        validators=[validate_names],
    )

    COLOR = (
        (5, _('White')),
        (4, _('Black')),
        (3, _('Yellow')),
        (2, _('Brown')),
        (1, _('Indigenous')),
    )
    ethnicity = models.IntegerField(
        _('Ethnicity'),
        choices=COLOR,
        help_text=_("Please insert the ethnicity of the patient"),
    )
    sus_number = models.CharField(
        _('SUS number'),
        help_text=_("Please, enter valid SUS in format: XXXXXXXXXXXXXXX"),
        unique=True,
        max_length=15,
        validators=[validate_sus],
    )
    civil_registry_of_birth = models.CharField(
        _('Civil register of birth'),
        help_text=_("Please, enter the civil registry of birth number"),
        unique=True,
        default='',
        max_length=11,
        validators=[validate_generic_number],
    )
    declaration_of_live_birth = models.CharField(
        _('Declaration of live birth'),
        help_text=_("Please, enter the declaration of live birth number"),
        unique=True,
        default='',
        max_length=11,
        validators=[validate_generic_number],
    )

    def have_procedures_almost_late(self):

        response = False

        if self.birthday_is_close():
            response = self.have_incomplete_procedures_on_current_age()

        return response

    def have_incomplete_procedures_on_current_age(self):
        from drdown.careline.models import Procedure

        current_age = self.user.age()
        proc_age = Procedure.convert_age_to_item(current_age)

        return self.checklist.procedure_set.filter(
            checkitem__age=proc_age,
            checkitem__required=True,
            checkitem__check=False,
        ).exists()

    def count_incomplete_procedures_for_current_age(self):
        from drdown.careline.models import Procedure

        current_age = self.user.age()
        proc_age = Procedure.convert_age_to_item(current_age)

        count = 0

        count += self.checklist.procedure_set.filter(
            checkitem__age=proc_age,
            checkitem__required=True,
            checkitem__check=False,
        ).count()

        count += self.checklist.procedure_set.filter(
            checkitem__age=proc_age,
            checkitem__when_needed=True,
            checkitem__check=False,
        ).count()

        return count

    def birthday_is_close(self):
        from drdown.careline.models import Procedure

        age = self.user.age()
        current_item = Procedure.convert_age_to_item(age)

        self.user.birthday += timezone.timedelta(days=31)

        future_age = self.user.age()
        future_item = Procedure.convert_age_to_item(future_age)

        self.user.birthday -= timezone.timedelta(days=31)

        return current_item is not future_item

    def __str__(self):
        return self.user.get_username()

    def clean(self, *args, **kwargs):

        try:
            user_db = Patient.objects.get(id=self.id).user

            if self.user != user_db:
                raise ValidationError(
                    _("Don't change users"))
            else:
                pass
        except Patient.DoesNotExist:
            pass

        self.user.clean()

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")


# runs every 1st day of a month
@periodic_task(run_every=crontab(day_of_month=[1, ]))
def careline_notification():

    target_patients = list(Patient.objects.all())
    target_patients = list(
        filter(
            lambda x: x.count_incomplete_procedures_for_current_age() > 0,
            target_patients
        )
    )

    for pat in target_patients:
        mail.send_patient_careline_status(pat)

    return target_patients


@receiver(post_save, sender=Patient)
def create_procedures(sender, instance, **kwargs):
    if not hasattr(instance, 'checklist'):
        apps.get_model('careline', 'Checklist') \
            .objects.create(patient=instance)


@receiver(post_save, sender=Patient)
def create_risk(sender, instance, **kwargs):
    if not hasattr(instance, 'risk'):
        apps.get_model('medicalrecords', 'Risk') \
            .objects.create(patient=instance)

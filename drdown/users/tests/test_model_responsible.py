from django.utils import timezone
from test_plus.test import TestCase
from ..admin import ResponsibleAdmin
from django.core.exceptions import ValidationError

from ..models import Responsible, Patient


class TestModelResponsible(TestCase):
    """
    Test if model Responsible is working correctly
    """

    def setUp(self):
        """
        This method will run before any test.
        """

        self.user_1 = self.make_user()
        self.user_2 = self.make_user(username="teste_2")

        self.responsible = Responsible.objects.create(
            cpf="974.220.200-16",
            user=self.user_1
        )

        self.patient = Patient.objects.create(
            ses="1234567",
            user=self.user_2,
            mother_name="Mãe",
            father_name="Pai",
            ethnicity=3,
            sus_number="12345678911",
            civil_registry_of_birth="12345678911",
            declaration_of_live_birth="12345678911",
            responsible=self.responsible
        )

    def test_get_absolute_url(self):
        """
        This test will get the absolute url of user.
        """

        self.assertEqual(
            self.user_1.get_absolute_url(),
            '/users/testuser/'
        )

    def test__str__(self):
        """
        This test check if __str__ is returning the data correctly.
        """

        self.assertEqual(
            self.responsible.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )

    def test_one_to_one_relation(self):
        """
        This test will check if the one_to_one relation is being respected.
        """

        self.assertIs(self.user_1, self.responsible.user)
        self.assertIs(self.responsible, self.user_1.responsible)

    def test_delete_cascade(self):
        """
        This test check if all object data is deleted along with it.
        """

        self.assertEquals(
            Responsible.objects.get(cpf="974.220.200-16"),
            self.responsible
        )

        self.user_1.delete()

        with self.assertRaises(Responsible.DoesNotExist):
            Responsible.objects.get(cpf="974.220.200-16")

    def test_patient_responsible_for_itself(self):
        """
         user 2 is the patient
         we will check if its not possible to set
         a patient as its responsible
        """

        self.assertIs(self.patient.user, self.user_2)

        with self.assertRaises(ValidationError):
            res = Responsible.objects.create(
                cpf="680.178.880-90",
                patient=self.patient,
                user=self.user_2
            )

    def test_readonly_user(self):
        """
        Test is user field is read_only after creation of an responsible
        """

        ma = ResponsibleAdmin(model=Responsible, admin_site=None)

        # since there is no atribute patient in self user, we
        # can assume that obj=None
        self.assertEqual(
            list(ma.get_readonly_fields(self, obj=None)),
            []
        )

        self.assertEqual(
            hasattr(self, 'responsible'),
            True
        )

        ma1 = ResponsibleAdmin(model=Responsible, admin_site=None)
        self.assertEqual(
            list(ma1.get_readonly_fields(self, obj=self.responsible)),
            ['user']
        )

    def test_patient_needs_attention(self):
        """
            Test if method produces correct response based on this responsible patient's checklist
        """

        today = timezone.datetime.today()

        self.patient.user.birthday = today - timezone.timedelta(days=365 + 29)
        self.patient.user.save()

        checklist = self.patient.checklist

        for procedure in checklist.procedure_set.all():
            for check_item in procedure.checkitem_set.all():
                check_item.check = True
                check_item.save()

        checklist.refresh_from_db()

        self.assertEquals(
            self.responsible.have_patient_needing_atention(),
            False
        )

        for procedure in checklist.procedure_set.all():
            for check_item in procedure.checkitem_set.all():
                check_item.check = False
                check_item.save()

        checklist.refresh_from_db()

        self.assertEquals(
            self.responsible.have_patient_needing_atention(),
            True
        )

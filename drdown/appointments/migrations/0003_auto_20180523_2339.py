# Generated by Django 2.0.3 on 2018-05-23 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_auto_20180523_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='speciality',
            field=models.CharField(choices=[('Speech Therapy', 'Speech Therapy'), ('Psychology', 'Psychology'), ('Physiotherapy', 'Physiotherapy'), ('Occupational Therapy', 'Occupational Therapy'), ('Cardiology', 'Cardiology'), ('Neurology', 'Neurology'), ('Pediatrics', 'Pediatrics'), ('General Practitioner', 'General Practitioner')], help_text='Speciality of appointment', max_length=30, verbose_name='Speciality'),
        ),
        migrations.AlterField(
            model_name='appointmentrequest',
            name='speciality',
            field=models.CharField(choices=[('Speech Therapy', 'Speech Therapy'), ('Psychology', 'Psychology'), ('Physiotherapy', 'Physiotherapy'), ('Occupational Therapy', 'Occupational Therapy'), ('Cardiology', 'Cardiology'), ('Neurology', 'Neurology'), ('Pediatrics', 'Pediatrics'), ('General Practitioner', 'General Practitioner')], help_text='Speciality of appointment', max_length=30, verbose_name='Speciality'),
        ),
    ]

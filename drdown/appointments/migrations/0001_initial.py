# Generated by Django 2.0.3 on 2018-05-01 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0015_auto_20180428_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift', models.CharField(choices=[('M', 'Morning'), ('A', 'Afternoon')], help_text='Shift of appointment', max_length=10, verbose_name='Shift')),
                ('date_time', models.DateTimeField(help_text='Date and time of appointment', max_length=50, verbose_name='Date and Time')),
                ('motive', models.TextField(help_text='Why are you requesting an appointment?', max_length=500, null=True, verbose_name='Motive')),
                ('speciality', models.CharField(choices=[('Speech Therapy', 'Speech Therapy'), ('Psychology', 'Psychology'), ('Physiotherapy', 'Physiotherapy'), ('Occupational Therapy', 'Occupational Therapy'), ('Doctor', 'Doctor'), ('Cardiology', 'Cardiology'), ('Neurology', 'Neurology'), ('Pediatrics', 'Pediatrics'), ('Nursing', 'Nursing')], help_text='Speciality of appointment', max_length=30, verbose_name='Speciality')),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('Canceled', 'Canceled'), ('Done', 'Done')], default='Scheduled', help_text='Is the appointment still scheduled?', max_length=20, verbose_name='Status')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='users.HealthTeam', verbose_name='Doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='users.Patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
            },
        ),
    ]

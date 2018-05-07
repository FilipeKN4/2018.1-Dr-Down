# Generated by Django 2.0.3 on 2018-05-07 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20180507_0027'),
        ('medicalrecords', '0002_complaint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='media/medicalrecords/exams', verbose_name='Exam')),
                ('day', models.DateTimeField(help_text='Day the exam was performed', verbose_name='Exam day')),
                ('status', models.IntegerField(choices=[(3, 'Executed'), (2, 'Collected'), (1, 'Marked examination')], help_text='Please, insert the status of the exam', verbose_name='Status')),
                ('name', models.CharField(max_length=200, verbose_name='Exam Name')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.HealthTeam', verbose_name='Author')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Exam',
                'verbose_name_plural': 'Exams',
            },
        ),
    ]

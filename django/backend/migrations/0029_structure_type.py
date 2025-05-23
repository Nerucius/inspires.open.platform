# Generated by Django 2.2 on 2019-10-07 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_evaluation_resend_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='structure_type',
            field=models.CharField(blank=True, choices=[('ACADEMIC_RESEARCH', 'Academic and/or Research'), ('CIVIL_SOCIETY_ORG', 'Civil Society Association'), ('NGO_NON_PROFIT', 'NGO and Non-Profit'), ('COMPANY', 'Company or For-Profit'), ('GOVERNMENT_ORG', 'Governmental Entity'), ('OTHER', 'Other')], max_length=254),
        ),
    ]

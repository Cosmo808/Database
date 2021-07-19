from django.db import models

# Create your models here.
class Patientbasicinfos(models.Model):
    id = models.CharField(db_column='ID', max_length=255, blank=True, null=False, primary_key=True)  # Field name made lowercase.
    checkdate = models.CharField(db_column='CheckDate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    checknumber = models.CharField(db_column='CheckNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    patientid = models.CharField(db_column='PatientID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    patientname = models.CharField(db_column='PatientName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)  # Field name made lowercase.
    age = models.CharField(db_column='Age', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clinicaldiagnosis = models.CharField(db_column='ClinicalDiagnosis', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    examinationfindings = models.CharField(db_column='ExaminationFindings', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    endoscopicdiagnosis = models.CharField(db_column='EndoscopicDiagnosis', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    pathologicaldiagnosis = models.CharField(db_column='PathologicalDiagnosis', max_length=255, blank=True, null=True)  # Field name made lowercase.
    patientreport = models.CharField(db_column='PatientReport', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hospitalid = models.CharField(db_column='HospitalID', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'patientbasicinfos'


class Administrator(models.Model):
    account = models.CharField(db_column='Account', max_length=255, blank=True, null=True)  # Field name made lowercase.
    passward = models.CharField(db_column='Passward', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'administrator'
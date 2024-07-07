from django.db import models

# Create your models here.
class Customers(models.Model):
    custid = models.AutoField(db_column='CustID', primary_key=True)  # Field name made lowercase.
    cname = models.CharField(db_column='CName', max_length=60, blank=True, null=True)  # Field name made lowercase.
    cemail = models.CharField(db_column='CEmail', unique=True, max_length=40, blank=True, null=True)  # Field name made lowercase.
    cpassword = models.CharField(db_column='CPassword', max_length=20, blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    deletedat = models.DateTimeField(db_column='DeletedAt', blank=True, null=True)  # Field name made lowercase.
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        managed = True
        db_table = 'customers'
from django.db import models

# Create your models here.


from django.db import models
from django.utils import timezone


class CdrProcess(models.Model):
    date = models.CharField(max_length=200, null=True)
    time = models.CharField(max_length=200, null=True)
    msisdn = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)
    gt = models.CharField(max_length=200, null=True)
    networkid = models.CharField(max_length=200, null=True)
    system = models.CharField(max_length=200, null=True)
    msc = models.CharField(max_length=200, null=True)
    imsi = models.CharField(max_length=200, null=True)
    error_msg = models.CharField(max_length=200, null=True)

    def __str__(self):
        #return "{}".format(self.msisdn)
        return "{}".format(self.msisdn)


class EsmeDlr(models.Model):
    date = models.CharField(max_length=200, null=True)
    time = models.CharField(max_length=200, null=True)
    networkid = models.CharField(max_length=200, null=True)
    senderid = models.CharField(max_length=200, null=True)
    msisdn = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)
    messageid = models.CharField(max_length=200, null=True)
    system = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.date, self.time, self.networkid, self.senderid, self.msisdn, self.status, self.networkid, self.system)
        # return "{}".format(self.msisdn)


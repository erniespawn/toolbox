from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now=True)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Toolbox(models.Model):
    date = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    msisdn = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    gt = models.CharField(max_length=200)
    networkid = models.CharField(max_length=200)
    system = models.CharField(max_length=200)

    def __str__(self):
        #return "{}".format(self.msisdn)
        return "{}, {}".format(self.id, self.system)
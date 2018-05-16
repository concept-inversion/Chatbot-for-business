from django.db import models


class FaqQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    category = models.CharField(max_length=50)


class UserQuery(models.Model):
    username = models.CharField(max_length=100)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    sem_sim = models.FloatField()
    probable_faq = models.ForeignKey(FaqQuestion,
                                     on_delete=models.CASCADE,
                                     related_name="faq")


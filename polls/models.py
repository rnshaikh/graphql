from django.db import models


class Question(models.Model):

    question_text = models.CharField(max_length=1024)
    pub_date = models.DateTimeField(auto_now_add=True)


class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=512)
    vote_count = models.IntegerField(default=0)


from django.db import models
from django.contrib.postgres.fields import JSONField


class LeadingQuestion(models.Model):
    data = models.JSONField()

class StoryStructure(models.Model):
    line = models.JSONField()
    name = models.CharField(max_length=255,null=True,blank=True)
    leading_question = models.ForeignKey(LeadingQuestion, on_delete=models.CASCADE,blank=True,null=True)


class AiIllustrationPrompt(models.Model):
    prompt = models.JSONField()
    leading_question = models.ForeignKey(LeadingQuestion, on_delete=models.CASCADE,blank=True,null=True)


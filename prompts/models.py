from django.db import models
from django.contrib.postgres.fields import JSONField

class LeadingQuestion(models.Model):
    data = models.JSONField()

class StoryStructure(models.Model):
    line = models.JSONField()

class AiIllustrationPrompt(models.Model):
    prompt = models.JSONField()

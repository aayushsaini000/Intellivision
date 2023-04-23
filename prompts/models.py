from django.db import models

class LeadingQuestion(models.Model):
    name = models.CharField(max_length=1000)
    question = models.CharField(max_length=2550)

class StoryStructure(models.Model):
    line = models.CharField(max_length=2550)

class AiIllustrationPrompt(models.Model):
    prompt = models.CharField(max_length=2550)

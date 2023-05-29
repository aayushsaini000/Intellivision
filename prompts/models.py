from django.db import models
from django.contrib.postgres.fields import JSONField


class LeadingQuestion(models.Model):
    data = models.JSONField()

class StoryStructure(models.Model):
    line = models.JSONField()
    name = models.CharField(max_length=255,null=True,blank=True)
    leading_question = models.ForeignKey(
        LeadingQuestion, on_delete=models.CASCADE,
        blank=True,null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class AiIllustrationPrompt(models.Model):
    prompt = models.JSONField()
    story = models.ForeignKey(
        StoryStructure, on_delete=models.CASCADE,
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class PromptRecord(models.Model):
    illustration_prompt = models.ForeignKey(
        AiIllustrationPrompt, on_delete=models.CASCADE,
        related_name="prompt_record"
    )
    prompt = models.CharField(max_length=500)
    image = models.ImageField(
        upload_to ='prompt_images/', null=True,
        blank=True, default=None
    )


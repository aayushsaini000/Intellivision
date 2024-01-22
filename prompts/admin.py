from django.contrib import admin
from .models import(
    LeadingQuestion, StoryStructure,
    AiIllustrationPrompt, PromptRecord
)

@admin.register(PromptRecord)
class PromptAdmin(admin.ModelAdmin):
    list_display = (
        "illustration_prompt", "prompt",
        "image"
    )

@admin.register(StoryStructure)
class StoryStructureAdmin(admin.ModelAdmin):
    list_display = ("name", "leading_question", "is_active")


@admin.register(LeadingQuestion)
class LeadingQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "data")


@admin.register(AiIllustrationPrompt)
class AiIllustrationPromptAdmin(admin.ModelAdmin):
    list_display = ("prompt", "story")

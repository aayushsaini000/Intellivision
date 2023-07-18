from django.contrib import admin
from .models import(
    LeadingQuestion, StoryStructure,
    AiIllustrationPrompt, PromptRecord
)

admin.site.register(LeadingQuestion)
admin.site.register(StoryStructure)
admin.site.register(AiIllustrationPrompt)

@admin.register(PromptRecord)
class PromptAdmin(admin.ModelAdmin):
    list_display = (
        "illustration_prompt", "prompt",
        "image"
    )

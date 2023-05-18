from django.contrib import admin
from .models import(
    LeadingQuestion, StoryStructure,
    AiIllustrationPrompt, PromptRecord
)

admin.site.register(LeadingQuestion)
admin.site.register(StoryStructure)
admin.site.register(AiIllustrationPrompt)
admin.site.register(PromptRecord)

from rest_framework import serializers
from .models import (
    LeadingQuestion, StoryStructure,
    AiIllustrationPrompt, PromptRecord
)
from datetime import datetime


class LeadingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadingQuestion
        fields = '__all__'

class StoryStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryStructure
        fields = '__all__'

class AiIllustrationPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiIllustrationPrompt
        fields = '__all__'


class PromptRecordListSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(
        source='created_at', format='%Y-%m-%d'
    )

    class Meta:
        model = AiIllustrationPrompt
        fields = (
            "id", "created_date", "is_active",
        )

class PromptRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromptRecord
        fields = (
            "id", "prompt", "image",
        )


class TemplateListSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(
        source='created_at', format='%Y-%m-%d'
    )
    class Meta:
        model = StoryStructure
        fields = (
            "id", "name", "created_date",
            "is_active"
        )
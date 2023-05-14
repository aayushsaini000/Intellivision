from rest_framework import serializers
from .models import LeadingQuestion, StoryStructure, AiIllustrationPrompt


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

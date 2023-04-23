from django.core.management.base import BaseCommand
from comic.models import LeadingQuestion, StoryStructure, AiIllustrationPrompt
from comic.utils import StoryTemplate


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        # Store leading questions
        LeadingQuestion.objects.all().delete()  # clear existing data
        for question in StoryTemplate().leading_questions:
            LeadingQuestion.objects.create(name=question['name'], question=question['question'])

        # Store story structure
        StoryStructure.objects.all().delete()  # clear existing data
        for line in StoryTemplate().story_structure:
            StoryStructure.objects.create(line=line)

        # Store AI illustration prompts
        AiIllustrationPrompt.objects.all().delete()  # clear existing data
        for prompt in StoryTemplate().ai_illustration_prompts:
            AiIllustrationPrompt.objects.create(prompt=prompt)

        self.stdout.write(self.style.SUCCESS('Successfully seeded data.'))

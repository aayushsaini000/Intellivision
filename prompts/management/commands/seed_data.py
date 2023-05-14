from django.core.management.base import BaseCommand
from prompts.models import LeadingQuestion, StoryStructure, AiIllustrationPrompt
from prompts.utils import StoryTemplate


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        # Store leading questions
        LeadingQuestion.objects.all().delete()  # clear existing data
        leadobj = LeadingQuestion.objects.create(data=StoryTemplate().leading_questions)

        # Store story structure
        StoryStructure.objects.all().delete()  # clear existing data
        StoryStructure.objects.create(line=StoryTemplate().story_structure,leading_question=leadobj)

        # Store AI illustration prompts
        AiIllustrationPrompt.objects.all().delete()  # clear existing data
        AiIllustrationPrompt.objects.create(prompt=StoryTemplate().ai_illustration_prompts,leading_question=leadobj)

        self.stdout.write(self.style.SUCCESS('Successfully seeded data.'))

import os
import subprocess

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Drops all tables and restores a PostgreSQL database from a text dump file'

    def add_arguments(self, parser):
        parser.add_argument('dump_path', type=str, help='The path to the dump file')
        parser.add_argument('--dbname', type=str, help='The database name', default=os.environ.get('NAME'))
        parser.add_argument('--user', type=str, help='The database user', default=os.environ.get('USER'))

    def restore_database(self, dump_path, dbname=os.environ.get('NAME'), user=os.environ.get('USER')):
        restore_command = f'psql -U {user} -d {dbname} -f {dump_path}'
        try:
            subprocess.run(restore_command, shell=True, check=True)
            self.stdout.write(self.style.SUCCESS(f'Successfully restored database "{dbname}" from "{dump_path}".'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR('Failed to restore the database.'))
            self.stdout.write(self.style.ERROR(str(e)))

    def handle(self, *args, **options):
        dump_path = options['dump_path']
        dbname = options['dbname']
        user = options['user']

        self.stdout.write(self.style.WARNING(f'Restoring database "{dbname}" from "{dump_path}"...'))
        self.restore_database(dump_path, dbname, user)

# class Command(BaseCommand):
#     help = 'Seed the database with initial data'

#     def handle(self, *args, **options):
#         # Store leading questions
#         LeadingQuestion.objects.all().delete()  # clear existing data
#         leadobj = LeadingQuestion.objects.create(data=StoryTemplate().leading_questions)

#         # Store story structure
#         StoryStructure.objects.all().delete()  # clear existing data
#         story = StoryStructure.objects.create(
#             line=StoryTemplate().story_structure,
#             leading_question=leadobj
#         )

#         # Store AI illustration prompts
#         AiIllustrationPrompt.objects.all().delete()  # clear existing data
#         AiIllustrationPrompt.objects.create(
#             prompt=StoryTemplate().ai_illustration_prompts,
#             story=story
#         )

#         self.stdout.write(self.style.SUCCESS('Successfully seeded data.'))


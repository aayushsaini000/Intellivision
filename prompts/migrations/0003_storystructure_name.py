# Generated by Django 4.2 on 2023-05-14 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prompts', '0002_aiillustrationprompt_leading_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storystructure',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
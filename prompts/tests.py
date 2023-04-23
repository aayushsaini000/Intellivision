#!/usr/bin/env python
# coding: utf-8

# In[1]:


import openai
from IPython.display import Image
# Set the API key
openai.api_key = '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'

class StoryTemplate:
    def __init__(self):
        self.leading_questions = [
            {'name': 'character', 'question': 'What is the name of the dog, the main character of the story?'},
            {'name': 'breed', 'question': 'What breed of dog is the dog?'},
            {'name': 'location', 'question': 'What city does the dog live in? (with a famous landmark)'},
            {'name': 'activity', 'question': "What is the dog's favorite activity? Fill in the blank: ___ing. Input your answer with 'ing'."},
            {'name': 'landmark', 'question': 'What is the landmark called?'},
            {'name': 'mean_character_name', 'question': 'Name the bad guy.'},
            {'name': 'mean_character_type', 'question': 'What kind of creature is the bad guy?'},
            {'name': 'savior', 'question': 'What is the name of the hero?'},
            {'name': 'savior_creature', 'question': 'What kind of creature is the hero?'},
            {'name': 'required_thing', 'question': 'What is something you need for {activity}?'},
        ]
        self.story_structure = [
            "Once upon a time there was a {breed} named {character}.",
            "{character} loved {activity} more than just about anything else.",
            "One day while they were {activity} outside of the {landmark},",
            "suddenly, {mean_character_name} the {mean_character_type} stole {character}'s {required_thing}.",
            "Luckily, {character} knew a {savior_creature} named {savior} who chased down {mean_character_name} and was able to get the {required_thing} back.",
            "Happy as can be, {character} was able to go {activity} again!",
        ]
        self.ai_illustration_prompts = [
            "{breed} dog {activity} in {location} in front of the {landmark} in the style of a coloring book illustration",
            "{mean_character_type} stealing {required_thing} for {activity} outside of {landmark} in {location} in the style of a coloring book illustration black and white only",
            "cartoon {savior_creature} super hero really cool in the style of a coloring book illustration black and white only",
            "cartoon very happy {breed} holding {required_thing} far away in a beautiful sunset in the style of a coloring book illustration. all black and white",
        ]

def create_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
    )
    image_url = response['data'][0]['url']

def picgen():
    story_template = StoryTemplate()

    # Get user inputs for each leading question.
    user_inputs = {}
    for question in story_template.leading_questions:
        answer = input(question['question'].format(**user_inputs) + ': ')
        user_inputs[question['name']] = answer

    # Print the story and display the images.
    for i, line in enumerate(story_template.story_structure):
    
        # Generate and display the image for each story part.
        if i < len(story_template.ai_illustration_prompts):
            prompt = story_template.ai_illustration_prompts[i].format(**user_inputs)
            create_image(prompt)

if __name__ == "__main__":
    picgen()


# %%

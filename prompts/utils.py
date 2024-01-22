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
            "cartoon very happy {breed} dog named {character} holding {required_thing} far away in a beautiful sunset in the style of a coloring book illustration. all black and white",
            "{breed} dog {character} {activity} in {location} in front of the {landmark} in the style of a coloring book illustration",
            "{mean_character_type} stealing {required_thing} for {activity} outside of {landmark} in {location} in the style of a coloring book illustration black and white only",
            "cartoon {savior_creature} super hero really cool in the style of a coloring book illustration black and white only",
            "{mean_character_name} the {mean_character_type} running away from {breed} dog {character} and {savior} in {location} in the style of a coloring book illustration black and white only",
            "{character} and {savior} high-fiving in front of the {landmark} after retrieving the {required_thing} in the style of a coloring book illustration"
        ]

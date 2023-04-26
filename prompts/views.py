import openai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LeadingQuestion, StoryStructure, AiIllustrationPrompt



openai.api_key = settings.OPENAI_API_KEY



class GeneratePicView(APIView):
    def post(self, request):
        # Get user inputs from the request body.
        user_inputs = {}
        for question in LeadingQuestion.objects.all():
            answer = request.data.get(question.name, '')
            user_inputs[question.name] = answer

        # Generate the story and images.
        response_data = {}
        for i, line in enumerate(StoryStructure.objects.all()):
            generated_text = line.line.format(**user_inputs)
            response_data[generated_text] = None

            if i < len(AiIllustrationPrompt.objects.all()):
                prompt = AiIllustrationPrompt.objects.all()[i].prompt.format(**user_inputs)
                image_url = self.create_image(prompt)
                response_data[generated_text] = image_url

        return Response(response_data)


    def create_image(self, prompt):
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        image_url = response['data'][0]['url']
        return image_url



class StoryQuestionsView(APIView):
    def get(self, request):
        questions = LeadingQuestion.objects.all().values('name', 'question')
        return Response(questions, status=status.HTTP_200_OK)





class PromptGenerator(APIView):
    def post(self, request, format=None):

        # Get the inputs from the request data
        input_data = request.data

        # Define the initial prompt with variable placeholders
        initial_prompt = ""
        for variable in input_data:
            initial_prompt += "{" + variable['name'] + "} "
            initial_prompt += variable['question'] + "\n"

        # Define the new prompt with improved text and variable placeholders
        new_prompt = "Improve this prompt but don't add any extra characters. Just make it more descriptive. Four sentences are required.\n\n{prompt}".format(
            prompt=initial_prompt
        )

        # Generate multiple prompts with the improved text
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=new_prompt,
            max_tokens=64,
            n=2,  # Request 2 completions
            stop=None,
            temperature=0.5,
        )
        print("8222",response.choices)

        # Convert the input data list to a dictionary
        input_dict = {}
        for variable in input_data:
            if 'value' in variable:
                input_dict[variable['name']] = variable['value']

        # Check that all variable names in input_dict are present in the initial prompt
        missing_variables = [variable['name'] for variable in input_data if variable['name'] not in initial_prompt]
        if missing_variables:
            return Response(f"Missing input for variables: {', '.join(missing_variables)}", status=status.HTTP_400_BAD_REQUEST)

        # Replace the variable placeholders in the generated prompts with the actual values
        choices = []
        for choice in response.choices:
            try:
            #     formatted_choice = choice.text.strip().format(**input_dict)
                choices.append(choice["text"])
            except KeyError as e:
                missing_variable = str(e).strip("'")
                return Response(f"Missing input for variable: {missing_variable}", status=status.HTTP_400_BAD_REQUEST)

        # Return the generated prompt choices
        return Response(choices)




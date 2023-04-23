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











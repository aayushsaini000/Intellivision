import openai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import(
    LeadingQuestion, StoryStructure,
    AiIllustrationPrompt, PromptRecord
)
from .serializers import (
    LeadingQuestionSerializer, StoryStructureSerializer,
    PromptRecordListSerializer, PromptRecordSerializer,
    TemplateListSerializer,
)
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
import requests


openai.api_key = settings.OPENAI_API_KEY



class GetStoriesView(APIView):
    def get(self, request):
        params = request.query_params
        if params.get("id", None):
            question = get_object_or_404(StoryStructure, pk=params["id"])
            questions_obj = StoryStructureSerializer(question).data
        else:
            questions = StoryStructure.objects.all()
            questions_obj = StoryStructureSerializer(questions,many=True).data
        return Response(questions_obj, status=status.HTTP_200_OK)

class GeneratePicView(APIView):
    def post(self, request):
        user_inputs = request.data

        try:
            ai_prompt = AiIllustrationPrompt.objects.get(id=request.data.get("id"))
            story_structure = StoryStructure.objects.get(leading_question=ai_prompt.leading_question)
        except AiIllustrationPrompt.DoesNotExist:
            return Response({"error": "No story exists with this ID"})
        except StoryStructure.DoesNotExist:
            return Response({"error": "No story exists with this leading_question"})

        response_data = []
        for i, line in enumerate(story_structure.line[:len(ai_prompt.prompt)]):
            generated_text = line.format(**user_inputs)
            prompt = ai_prompt.prompt[i].format(**user_inputs)
            image_url = self.create_image(ai_prompt, prompt)
            response_data.append({"prompt": generated_text, "image": image_url})

        return Response(response_data)

    def create_image(self, instance, prompt):
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        image_url = response['data'][0]['url']
        content = requests.get(image_url).content
        image_file = ContentFile(content)
        record = PromptRecord.objects.create(
            illustration_prompt=instance,
            prompt=prompt
        )
        record.image.save(f"prompt_{instance.id}.jpg", image_file)
        return image_url



class StoryQuestionsView(APIView):
    def get(self, request):
        objid = request.GET.get("id")
        try:
            questions = LeadingQuestion.objects.get(id=objid)
        except Exception:
            return Response({"error":"no question available by given id"})
        questions_obj = LeadingQuestionSerializer(questions).data
        return Response(questions_obj, status=status.HTTP_200_OK)





class PromptGenerator(APIView):
    def post(self, request, format=None):

        # Get the inputs from the request data
        input_data = request.data.get("input_data")
        template_name = request.data.get("template_name")

        # Define the initial prompt with variable placeholders
        initial_prompt = ""
        for variable in input_data:
            initial_prompt += "{" + variable['name'] + "} "
            initial_prompt += variable['question'] + "\n"

        question_instance, _ = LeadingQuestion.objects.get_or_create(
            data=input_data
        )


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
        
        StoryStructure.objects.create(
            line=choice,
            name=template_name,
            leading_question=question_instance
        )

        # Return the generated prompt choices
        return Response(choices)


class PromptRecordView(APIView):

    def get(self, request, pk=None):
        params = request.query_params
        if params.get("id", None):
            question = get_object_or_404(AiIllustrationPrompt, pk=params["id"])
            questions_obj = PromptRecordSerializer(
                question.prompt_record.all(),
                many=True, context={"request": request}
            ).data
        else:
            questions = AiIllustrationPrompt.objects.all()
            questions_obj = PromptRecordListSerializer(questions,many=True).data
        return Response(questions_obj, status=status.HTTP_200_OK)


class TemplateListView(APIView):

    def get(self, request, pk=None):
        params = request.query_params
        if params.get("id", None):
            instance = get_object_or_404(
                StoryStructure, pk=params.get("id")
            )
            serializer = TemplateListSerializer(
                instance
            ).data
        else:
            queryset = StoryStructure.objects.all()
            serializer = TemplateListSerializer(
                queryset, many=True
            ).data
        return Response(serializer)
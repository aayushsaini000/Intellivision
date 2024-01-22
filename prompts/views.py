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
    TemplateListSerializer, SaveTemplateSerializer,
    ManageTemplateSerializer, SubmitReviewSerializer
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
            questions = StoryStructure.objects.all().order_by("-id")
            questions_obj = StoryStructureSerializer(questions,many=True).data
        return Response(questions_obj, status=status.HTTP_200_OK)


class GeneratePicView(APIView):
    def post(self, request):
        user_inputs = request.data
        email = request.data.get("email")
        try:
            story_structure = StoryStructure.objects.get(id=request.data.get("id"))
            ai_prompt = AiIllustrationPrompt.objects.get(story=story_structure)
        except AiIllustrationPrompt.DoesNotExist:
            return Response({"error": "No story exists with this ID"})
        except StoryStructure.DoesNotExist:
            return Response({"error": "No story exists with this leading_question"})

        response_data = []
        try:
            for i, line in enumerate(story_structure.line[:len(ai_prompt.prompt)]):
                generated_text = line.format(**user_inputs)
                prompt = ai_prompt.prompt[i].format(**user_inputs)
                # image_url = self.create_image(ai_prompt, generated_text)
                image_url = self.create_image(ai_prompt, prompt,email)
                response_data.append({"prompt": prompt, "image": image_url})
        except KeyError as e:
            return Response(
                {
                    "message": f"veriable {str(e)} requireds"
                }
            )

        except Exception as e:
            return Response(
                {
                    "message": f"{str(e)}"
                }
            )

        return Response(response_data)

    def create_image(self, instance, prompt, email):

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
            prompt=prompt,
            email = email
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

        # Define the initial prompt with variable placeholders
        initial_prompt = ""
        for variable in input_data:
            initial_prompt += "{" + variable['name'] + "} "
            initial_prompt += variable['question'] + "\n"

        # Define the new prompt with improved text and variable placeholders
        new_prompt = "Improve this prompt but don't add any extra characters. Just make it more descriptive. Four sentences with lowercase words only are required with the given keywords in curly braces. Make sure do not add any new keyword in curly braces other then given keywords\n\n{prompt}".format(
            prompt=initial_prompt
        )

        # Generate multiple prompts with the improved text
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
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
                choices.append(
                    {
                        "story_text": choice["text"]
                    }
                )
            except KeyError as e:
                missing_variable = str(e).strip("'")
                return Response(f"Missing input for variable: {missing_variable}", status=status.HTTP_400_BAD_REQUEST)
        
        # Return the generated prompt choices
        return Response(
            {
                "data": choices
            }
        )


class SaveTemplateView(APIView):
    def post(self, request, format=None):

        serializer = SaveTemplateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Get the inputs from the request data
        input_data = serializer.validated_data["input_data"]
        template_name = serializer.validated_data["template_name"]
        template_text = serializer.validated_data["template_text"]

        question_instance, _ = LeadingQuestion.objects.get_or_create(
            data=input_data
        )

        initial_prompt = ""
        for variable in input_data:
            initial_prompt += "{" + variable['name'] + "} "
            initial_prompt += variable['question'] + "\n"

        try:
            line = [template_text[0].get("story_text").replace("\n", "")]
        except:
            line = [template_text[0].replace("\n", "")]

        story = StoryStructure.objects.create(
            line=line,
            name=template_name,
            leading_question=question_instance
        )
        AiIllustrationPrompt.objects.create(
            prompt=[initial_prompt.replace("\n", "")],
            story=story
        )
        

        return Response(
            {
                "message": "Template saved successfully"
            }
        )


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


class ManageTemplateView(APIView):

    def get(self, request, pk=None):
        params = request.query_params
        if params.get("id", None):
            instance = get_object_or_404(
                StoryStructure, pk=params.get("id"),
            )
            serializer = TemplateListSerializer(
                instance
            ).data
        else:
            queryset = StoryStructure.objects.all().order_by("-id")
            serializer = TemplateListSerializer(
                queryset, many=True
            ).data
        return Response(serializer)

    def post(self, request):
        serilaizer = ManageTemplateSerializer(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        instance = get_object_or_404(
            StoryStructure, pk=serilaizer.validated_data["id"],
        )
        instance.is_active=serilaizer.validated_data["is_active"]
        instance.save()
        return Response(
            {
                "message": "Updated successfully"
            }
        )


class SubmitReviewView(APIView):

    def post(self, request):
        serializer = SubmitReviewSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Sent successfully"
            }
        )




from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import PromptRecord
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
import io
import os
from django.conf import settings

# def generate_pdf(records):
#     buffer = io.BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)
#     width, height = letter

#     x_offset = 50
#     y_offset = height - 50
#     image_height = 150

#     for record in records:
#         c.drawString(x_offset, y_offset, record['prompt'])
#         y_offset -= 20

#         image_path = os.path.join(settings.MEDIA_ROOT, record['image'])
#         try:
#             img = Image(image_path)
#             img.drawHeight = image_height
#             img.drawWidth = image_height * img.imageWidth / img.imageHeight
#             img.wrapOn(c, width, height)
#             img.drawOn(c, x_offset, y_offset - img.drawHeight)
#             y_offset -= (img.drawHeight + 20)
#         except Exception as e:
#             print(f"Error loading image {image_path}: {e}")

#         if y_offset < 100:
#             c.showPage()
#             y_offset = height - 50

#     c.save()
#     buffer.seek(0)
#     return buffer



def pdf_view(request, email):
    time_threshold = timezone.now() - timedelta(seconds=300)
    records = PromptRecord.objects.filter(email=email, created_at__gt=time_threshold).order_by('-created_at').values('prompt', 'image')
    # print("37333",list(records))
    # Assuming records are in the format you provided and images are accessible
    pdf = generate_pdf(list(records))
    # print("37666",pdf)
    # Email setup
    subject = 'Your story file'
    message = 'Please find attached the PDF of your Story.'
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
    email.attach('prompt_records.pdf', pdf.getvalue(), 'application/pdf')
    email.send()

    return HttpResponse("Email sent successfully.")






from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
import io
import os
from django.conf import settings

def generate_pdf(records):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x_offset = 50
    y_offset = height - 50
    image_height = 150

    for record in records:
        c.drawString(x_offset, y_offset, record['prompt'])
        y_offset -= 20  # Adjust based on the height of your text

        image_path = os.path.join(settings.MEDIA_ROOT, record['image'])
        try:
            img = Image(image_path)
            # Maintain aspect ratio but increase width by 50%
            aspect_ratio = img.imageWidth / img.imageHeight
            img.drawHeight = image_height
            img.drawWidth = img.drawHeight * aspect_ratio * 1.5  # Increase width by 50%
            img.wrapOn(c, width, height)
            img.drawOn(c, x_offset, y_offset - img.drawHeight)
            y_offset -= (img.drawHeight + 20)  # Adjust for spacing between images
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")

        if y_offset < 100:  # Arbitrary threshold for page break
            c.showPage()
            y_offset = height - 50  # Reset y_offset for the new page

    c.save()
    buffer.seek(0)
    return buffer



# from django.http import HttpResponse, FileResponse
# from django.utils import timezone
# from datetime import timedelta
# from .models import PromptRecord
# import io


# def pdf_view(request, email):
#     time_threshold = timezone.now() - timedelta(seconds=60000000000)
#     records = PromptRecord.objects.filter(email=email, created_at__gt=time_threshold).order_by('-created_at').values('prompt', 'image')

#     # Generate PDF from records
#     pdf_buffer = generate_pdf(list(records))

#     # Instead of sending an email, return the PDF as a response for the user to download
#     # Set the content type and disposition to indicate attachment
#     response = FileResponse(pdf_buffer, as_attachment=True, filename='prompt_records.pdf', content_type='application/pdf')
#     return response

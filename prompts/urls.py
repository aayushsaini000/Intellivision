from django.urls import path

from .views import (
    GeneratePicView, StoryQuestionsView, PromptGenerator,
    GetStoriesView, PromptRecordView, ManageTemplateView,
    SaveTemplateView, SubmitReviewView,pdf_view
)

urlpatterns = [
    path('generate-image/', GeneratePicView.as_view()),
    path('generate-template/', PromptGenerator.as_view()),
    path('get-questions/', StoryQuestionsView.as_view()),
    path('get-stories/', GetStoriesView.as_view()),
    path('prompt-record/', PromptRecordView.as_view()),
    path('template/', ManageTemplateView.as_view()),
    path('template-save/', SaveTemplateView.as_view()),
    path('send-review/', SubmitReviewView.as_view()),
    path('generate_pdf/<str:email>/', pdf_view, name='generate_pdf'),
]

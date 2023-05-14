from django.urls import path

from .views import GeneratePicView,StoryQuestionsView,PromptGenerator,GetStoriesView

urlpatterns = [
    path('generate-image/', GeneratePicView.as_view()),
    path('get-questions/', StoryQuestionsView.as_view()),
    path('generate-template/', PromptGenerator.as_view()),
    path('get-stories/', GetStoriesView.as_view()),

]
from django.urls import path

from .views import GeneratePicView,StoryQuestionsView

urlpatterns = [
    path('generate-image/', GeneratePicView.as_view()),
    path('get-questions/', StoryQuestionsView.as_view()),

]
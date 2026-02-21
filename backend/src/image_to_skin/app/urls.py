from django.urls import path

from image_to_skin.app.views import GenerationResultView, StartGenerationView

urlpatterns = [
    path('generation/start', StartGenerationView.as_view()),
    path('generation/<str:task_id>', GenerationResultView.as_view()),
]

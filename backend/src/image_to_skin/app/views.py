import base64

from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_q.tasks import async_task

from image_to_skin.app.models import GenerationTask


class StartGenerationView(APIView):
    def post(self, request):
        image_data = request.data.get('image')
        if not image_data:
            return Response({'error': 'Missing image field.'}, status=status.HTTP_400_BAD_REQUEST)

        image_data = image_data.split(',')[1]

        try:
            input_bytes = base64.b64decode(image_data)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid base64 image.'}, status=status.HTTP_400_BAD_REQUEST)

        task = GenerationTask.objects.create(input_image=input_bytes)
        async_task('image_to_skin.app.tasks.process_generation_task', task.id)

        return Response({'id': task.id}, status=status.HTTP_202_ACCEPTED)


class GenerationResultView(APIView):
    def get(self, request, task_id):
        try:
            task = GenerationTask.objects.get(pk=task_id)
        except GenerationTask.DoesNotExist:
            raise Http404('Generation task not found.')

        if not task.output_image:
            return Response({'error': 'Output not ready.'}, status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(task.output_image, content_type='image/png')

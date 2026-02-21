from django.db import models
from django.utils.crypto import get_random_string


def generate_hashid() -> str:
    return get_random_string(16)


class GenerationTask(models.Model):
    id = models.CharField(primary_key=True, max_length=16, default=generate_hashid, editable=False)
    input_image = models.BinaryField()
    output_image = models.BinaryField(null=True, blank=True)

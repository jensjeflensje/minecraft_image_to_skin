from django.db import migrations, models
import image_to_skin.app.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='GenerationTask',
            fields=[
                ('id', models.CharField(default=image_to_skin.app.models.generate_hashid, editable=False, max_length=16, primary_key=True, serialize=False)),
                ('input_image', models.BinaryField()),
                ('output_image', models.BinaryField(blank=True, null=True)),
            ],
        ),
    ]

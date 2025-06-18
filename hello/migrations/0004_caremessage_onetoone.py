from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('hello', '0003_caremessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caremessage',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='care_message', to='hello.customuser'),
        ),
    ]

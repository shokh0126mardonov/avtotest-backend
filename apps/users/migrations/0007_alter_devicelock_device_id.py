# Generated manually on 2026-04-26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_devicelock_telegram_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devicelock",
            name="device_id",
            field=models.CharField(max_length=255, null=True),
        ),
    ]

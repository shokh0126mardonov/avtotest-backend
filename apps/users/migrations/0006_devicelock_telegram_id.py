# Generated manually on 2026-04-26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_devicelock_user_agent_alter_user_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="devicelock",
            name="telegram_id",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]

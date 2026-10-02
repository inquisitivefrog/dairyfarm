from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0002_extend_years_to_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annual',
            name='link',
            field=models.URLField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='monthly',
            name='link',
            field=models.URLField(max_length=100, null=True),
        ),
    ]

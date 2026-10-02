from django.db import migrations, models


REPORT_YEARS = [
    (2015, '2015'),
    (2016, '2016'),
    (2017, '2017'),
    (2018, '2018'),
    (2019, '2019'),
    (2020, '2020'),
    (2021, '2021'),
    (2022, '2022'),
    (2023, '2023'),
    (2024, '2024'),
    (2025, '2025'),
    (2026, '2026'),
]


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annual',
            name='year',
            field=models.SmallIntegerField(
                choices=REPORT_YEARS,
                default=2015,
            ),
        ),
        migrations.AlterField(
            model_name='monthly',
            name='year',
            field=models.SmallIntegerField(
                choices=REPORT_YEARS,
                default=2015,
            ),
        ),
    ]

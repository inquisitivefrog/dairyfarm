# Generated by Django 2.0.1 on 2018-01-26 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Age',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('breed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Breed')),
            ],
        ),
        migrations.CreateModel(
            name='Cow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField(auto_now_add=True)),
                ('age', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Age')),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Breed')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Color')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=50, unique=True)),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Breed')),
            ],
        ),
        migrations.AddField(
            model_name='cow',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Image'),
        ),
        migrations.AddField(
            model_name='cow',
            name='purchased_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.0.1 on 2018-02-13 20:57

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
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
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
            name='BreedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=50, unique=True)),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Breed')),
            ],
        ),
        migrations.CreateModel(
            name='CerealHay',
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
                ('purchase_date', models.DateField()),
                ('age', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Age')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Color')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.BreedImage')),
                ('purchased_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Action')),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Cow')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('distance', models.IntegerField(default=0)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Cow')),
            ],
        ),
        migrations.CreateModel(
            name='GrassHay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='%Y-%m-%d %H:%M:%S')),
                ('temperature', models.FloatField(default=1.0)),
                ('respiratory_rate', models.FloatField(default=1.0)),
                ('heart_rate', models.FloatField(default=1.0)),
                ('blood_pressure', models.FloatField(default=1.0)),
                ('weight', models.IntegerField(default=0)),
                ('body_condition_score', models.FloatField(default=1.0)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Cow')),
            ],
        ),
        migrations.CreateModel(
            name='Illness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(max_length=20, unique=True)),
                ('treatment', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(max_length=20, unique=True)),
                ('treatment', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LegumeHay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Milk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('gallons', models.SmallIntegerField(default=0)),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Cow')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pasture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fallow', models.BooleanField(default=False)),
                ('distance', models.IntegerField(default=0)),
                ('cereal_hay', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.CerealHay')),
                ('grass_hay', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.GrassHay')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=50, unique=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='pasture',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.RegionImage'),
        ),
        migrations.AddField(
            model_name='pasture',
            name='legume_hay',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.LegumeHay'),
        ),
        migrations.AddField(
            model_name='pasture',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Season'),
        ),
        migrations.AddField(
            model_name='pasture',
            name='seeded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='healthrecord',
            name='illness',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Illness'),
        ),
        migrations.AddField(
            model_name='healthrecord',
            name='injury',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Injury'),
        ),
        migrations.AddField(
            model_name='healthrecord',
            name='recorded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='healthrecord',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Status'),
        ),
        migrations.AddField(
            model_name='healthrecord',
            name='vaccine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Vaccine'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='pasture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Pasture'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='recorded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
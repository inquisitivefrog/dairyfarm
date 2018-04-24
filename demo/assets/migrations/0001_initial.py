# Generated by Django 2.0.1 on 2018-04-24 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


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
                ('name', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=50)),
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
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('join_date', models.DateField()),
                ('inactive_date', models.DateField(default='2100-12-31')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('purchase_date', models.DateField()),
                ('sell_date', models.DateField(default='2100-12-31')),
                ('link', models.URLField(max_length=50, null=True)),
                ('age', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Age')),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Breed')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Client')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Color')),
                ('purchased_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_time', models.DateTimeField()),
                ('link', models.URLField(max_length=50, null=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Action')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Client')),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Cow')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_time', models.DateTimeField()),
                ('link', models.URLField(max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Client')),
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
                ('inspection_time', models.DateTimeField()),
                ('temperature', models.FloatField(default=1.0)),
                ('respiratory_rate', models.FloatField(default=1.0)),
                ('heart_rate', models.FloatField(default=1.0)),
                ('blood_pressure', models.FloatField(default=1.0)),
                ('weight', models.IntegerField(default=0)),
                ('body_condition_score', models.FloatField(default=1.0)),
                ('link', models.URLField(max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Client')),
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
                ('milking_time', models.DateTimeField()),
                ('gallons', models.SmallIntegerField(default=0)),
                ('link', models.URLField(max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Client')),
                ('cow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Cow')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pasture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('url', models.CharField(max_length=50, unique=True)),
                ('fallow', models.BooleanField(default=False)),
                ('distance', models.IntegerField(default=0)),
                ('link', models.URLField(max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.SmallIntegerField(default=2015)),
                ('link', models.URLField(max_length=50, null=True)),
                ('cereal_hay', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.CerealHay')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Client')),
                ('grass_hay', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.GrassHay')),
                ('legume_hay', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.LegumeHay')),
                ('pasture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Pasture')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Season')),
                ('seeded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
            name='treatment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Treatment'),
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

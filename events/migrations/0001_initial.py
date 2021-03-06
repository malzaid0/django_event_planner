# Generated by Django 2.2.5 on 2020-09-20 23:46

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
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=300)),
                ('datetime', models.DateTimeField()),
                ('seats', models.PositiveSmallIntegerField()),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendant', models.ManyToManyField(related_name='events', to=settings.AUTH_USER_MODEL)),
                ('event', models.ManyToManyField(related_name='attendance', to='events.Event')),
            ],
        ),
    ]

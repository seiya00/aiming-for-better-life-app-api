# Generated by Django 3.2.18 on 2023-03-31 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_meal'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vegetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vegetable', models.CharField(max_length=255, unique=True)),
                ('color', models.CharField(max_length=255)),
                ('varieties', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='meal',
            name='could_control_appetite',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='fried_food',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='processed_food',
        ),
        migrations.AddField(
            model_name='meal',
            name='answer_bool',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='answer_choice',
            field=models.CharField(choices=[('none', '無し'), ('a bit', '少し'), ('normal', '普通'), ('a lot', 'たくさん')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='answer_int',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='answer_type',
            field=models.CharField(default=False, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meal',
            name='is_allergy',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', '男性'), ('female', '女性'), ('other', '回答なし')], max_length=10),
        ),
        migrations.AddField(
            model_name='meal',
            name='meal_question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.mealquestion'),
        ),
        migrations.AddField(
            model_name='meal',
            name='vegetable_question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.vegetable'),
        ),
    ]
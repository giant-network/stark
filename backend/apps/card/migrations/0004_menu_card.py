# Generated by Django 2.1.7 on 2019-03-29 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0003_menu_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='card.Card', verbose_name='卡片'),
        ),
    ]

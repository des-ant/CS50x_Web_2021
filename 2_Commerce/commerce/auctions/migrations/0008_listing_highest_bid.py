# Generated by Django 3.2.5 on 2021-07-26 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210725_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='highest_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winners', to='auctions.bid'),
        ),
    ]
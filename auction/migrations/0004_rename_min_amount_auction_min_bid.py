# Generated by Django 4.1.1 on 2022-10-17 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auction", "0003_auction_min_amount"),
    ]

    operations = [
        migrations.RenameField(
            model_name="auction", old_name="min_amount", new_name="min_bid",
        ),
    ]

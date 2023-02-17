# Generated by Django 4.1.7 on 2023-02-14 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_discount_options_alter_item_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Discount',
            new_name='discount',
        ),
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('USD', 'Dollars'), ('EUR', 'Euros')], default='USD', max_length=3),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]

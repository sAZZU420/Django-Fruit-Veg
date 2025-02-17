# Generated by Django 5.0.6 on 2024-07-11 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('COMPLETED', 'COMPLETED'), ('VALID', 'VALID'), ('DUE', 'DUE'), ('ACCEPTED', 'ACCEPTED'), ('CANCELLED', 'CANCELLED')], default='NEW', max_length=50),
        ),
    ]

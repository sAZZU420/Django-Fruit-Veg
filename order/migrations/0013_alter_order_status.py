# Generated by Django 5.0.6 on 2024-07-11 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CANCELLED', 'CANCELLED'), ('COMPLETED', 'COMPLETED'), ('NEW', 'NEW'), ('DUE', 'DUE'), ('ACCEPTED', 'ACCEPTED'), ('VALID', 'VALID')], default='NEW', max_length=50),
        ),
    ]

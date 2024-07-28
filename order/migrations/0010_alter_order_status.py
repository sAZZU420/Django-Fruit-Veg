# Generated by Django 5.0.6 on 2024-07-11 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('VALID', 'VALID'), ('DUE', 'DUE'), ('CANCELLED', 'CANCELLED'), ('COMPLETED', 'COMPLETED'), ('NEW', 'NEW')], default='NEW', max_length=50),
        ),
    ]
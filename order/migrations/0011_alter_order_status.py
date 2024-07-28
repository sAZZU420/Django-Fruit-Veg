# Generated by Django 5.0.6 on 2024-07-11 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('DUE', 'DUE'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED'), ('VALID', 'VALID'), ('NEW', 'NEW')], default='NEW', max_length=50),
        ),
    ]
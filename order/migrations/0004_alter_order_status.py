# Generated by Django 5.0.6 on 2024-07-11 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('COMPLETED', 'COMPLETED'), ('ACCEPTED', 'ACCEPTED'), ('CANCELLED', 'CANCELLED'), ('VALID', 'VALID'), ('DUE', 'DUE')], default='NEW', max_length=50),
        ),
    ]
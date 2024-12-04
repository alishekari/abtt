# Generated by Django 5.1.3 on 2024-12-04 00:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdrawable_balance', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_created_at', models.DateTimeField(auto_now_add=True)),
                ('_updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('credit', 'بستانکار'), ('debit', 'بدهکار')], max_length=8)),
                ('comment', models.CharField(blank=True, max_length=1024, null=True)),
                ('tracking_code', models.CharField(blank=True, max_length=128, null=True)),
                ('balance', models.IntegerField(default=0)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.order')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statements', to='wallet.wallet')),
            ],
            options={
                'ordering': ('-_created_at',),
            },
        ),
    ]

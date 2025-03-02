# Generated by Django 5.1.3 on 2024-12-26 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('balance_after_trxn', models.DecimalField(decimal_places=2, max_digits=12)),
                ('transaction_type', models.IntegerField(choices=[(1, 'Deposit'), (2, 'Withdrawal'), (3, 'Loan'), (4, 'Loan Repayment')], null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('loan_approval', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.userbankaccount')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]

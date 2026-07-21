from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_product_alter_order_options_order_notes_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('tmoney', 'Mixx by Yas'), ('flooz', 'Flooz'), ('card', 'Carte bancaire'), ('cash', 'Espèces')], max_length=20),
        ),
    ]

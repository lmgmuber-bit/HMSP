from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', 'last_migration_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='suscripcion',
            name='nombre',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='suscripcion',
            name='telefono',
            field=models.CharField(max_length=20, blank=True, default=''),
            preserve_default=False,
        ),
    ]

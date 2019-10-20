# Generated by Django 2.2.5 on 2019-10-14 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_vaalit', '0003_virka_read_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kysymys',
            name='to_virka',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='app_vaalit.Virka'),
        ),
        migrations.AlterField(
            model_name='vastaus',
            name='by_ehdokas',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='answered_by', to='app_vaalit.Ehdokas'),
        ),
        migrations.AlterField(
            model_name='vastaus',
            name='to_question',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app_vaalit.Kysymys'),
        ),
    ]

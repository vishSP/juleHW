# Generated by Django 4.2.3 on 2023-07-26 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название урока')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='lesson/', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='описание')),
                ('link', models.CharField(max_length=200, verbose_name='ссылка на видео')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payday', models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='сумма оплаты')),
                ('payment_type', models.CharField(choices=[('cash', 'Наличные'), ('card', 'Перевод на счет')], default='card', max_length=10, verbose_name='способ оплаты')),
                ('payment_intent_id', models.CharField(blank=True, max_length=500, null=True, verbose_name='ID намерения платежа')),
                ('payment_method_id', models.CharField(blank=True, max_length=500, null=True, verbose_name='ID метода платежа')),
                ('status', models.CharField(blank=True, max_length=50, null=True, verbose_name='cтатус платежа')),
                ('confirmation', models.BooleanField(default=False, verbose_name='подтверждение платежа')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
            },
        ),
        migrations.CreateModel(
            name='Сourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название курса')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='course/', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='описание')),
                ('price', models.IntegerField(default=5000, verbose_name='стоимость курса')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='статус подписки')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinsky.сourse', verbose_name='курс')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinsky.payments', verbose_name='платеж')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddField(
            model_name='payments',
            name='paid_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vinsky.сourse', verbose_name='оплаченный курс'),
        ),
        migrations.AddField(
            model_name='payments',
            name='paid_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vinsky.lesson', verbose_name='оплаченный урок'),
        ),
        migrations.AddField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vinsky.сourse', verbose_name='курс'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
    ]


from django.db import models
from config import settings
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Сourse(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Изображение')
    text = models.TextField(verbose_name='описание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='автор')
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название урока')
    preview = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='Изображение')
    text = models.TextField(verbose_name='описание')
    link = models.CharField(max_length=200, verbose_name='ссылка на видео')
    course = models.ForeignKey(Сourse, on_delete=models.CASCADE, **NULLABLE, verbose_name='курс')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='автор')
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    paid_course = models.ForeignKey(Сourse, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='оплаченный урок')

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='пользователь')
    payday = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Перевод на счет'),

    ]
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='card', verbose_name='способ оплаты'
                                    )

    def __str__(self):
        return f'{self.paid_course if self.paid_course else self.paid_lesson}, {self.payday} ,{self.payment_type}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'



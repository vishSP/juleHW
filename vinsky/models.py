
from django.db import models
from config import settings
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Сourse(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Изображение')
    text = models.TextField(verbose_name='описание')
    price = models.IntegerField(default=5000, verbose_name='стоимость курса')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='автор')
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='автор')
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

    payment_intent_id = models.CharField(max_length=500, **NULLABLE, verbose_name='ID намерения платежа')
    payment_method_id = models.CharField(max_length=500, **NULLABLE, verbose_name='ID метода платежа')
    status = models.CharField(max_length=50, **NULLABLE, verbose_name='cтатус платежа')
    confirmation = models.BooleanField(default=False, verbose_name='подтверждение платежа')

    def __str__(self):
        return f'{self.paid_course if self.paid_course else self.paid_lesson}, {self.payday} ,{self.payment_type}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    course = models.ForeignKey(Сourse, on_delete=models.CASCADE, verbose_name='курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE, verbose_name='платеж')
    status = models.BooleanField(default=False, verbose_name='статус подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} - {self.course}: {self.status}'
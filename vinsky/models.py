from django.db import models
NULLABLE = {'blank': True, 'null': True}

class Сourse(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Изображение')
    text = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='Изображение')
    text = models.TextField(verbose_name='описание')
    link = models.CharField(max_length=200, verbose_name='ссылка на видео')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
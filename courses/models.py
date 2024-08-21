from django.db import models

from product import settings


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        verbose_name='Название группы',
        max_length=100,
        null=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='GroupCustomUsers',
        related_name='group'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)


class GroupCustomUsers(models.Model):
    """Модель связывает группы и пользователей."""

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='group_users'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_users'
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время вступления'
    )

    class Meta:
        unique_together = ('group', 'user')
        verbose_name = 'Связь группы и пользователя'
        verbose_name_plural = 'Связи групп и пользователей'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user.get_full_name()} в {self.group.title}'

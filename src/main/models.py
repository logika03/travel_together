from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager as DjangoUserManager
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True


class UserManager(DjangoUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(email=email, is_superuser=True)
        user.set_password(password)
        user.save()
        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(default=None, verbose_name='Фото профиля')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=12, unique=True, verbose_name='Номер телефона')
    location = models.CharField(max_length=30, default='Казань', verbose_name='Местоположение')

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return self.is_superuser


class Transport(BaseModel):
    title = models.CharField(max_length=20, verbose_name='Название')

    class Meta:
        verbose_name = 'транспорт'
        verbose_name_plural = 'транспорты'

    def __str__(self):
        return self.title


class Trip(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    description = models.TextField(verbose_name='Описание')
    transport = models.ManyToManyField(Transport, verbose_name='Транспорт')
    is_available = models.BooleanField(default=True, verbose_name='Доступна')
    country = models.CharField(max_length=50, verbose_name='Страна')
    city = models.CharField(max_length=50, verbose_name='Город')
    city_information = models.URLField(max_length=200, verbose_name='Информация о городе')
    date = models.DateField(verbose_name='Дата поездки')

    class Meta:
        verbose_name = 'поездка'
        verbose_name_plural = 'поездки'

    def __str__(self):
        return f'{self.country}, {self.city}'


class TravelParticipant(BaseModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name='Поездка', related_name='participants')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Участник',
                                    related_name='trips_participants')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')

    class Meta:
        verbose_name = 'участник поездки'
        verbose_name_plural = 'участники поездки'

    def __str__(self):
        return f'{self.participant.first_name} {self.participant.last_name}'


class Dialog(BaseModel):
    first_participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first',
                                          verbose_name='Первый собеседник')
    second_participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second',
                                           verbose_name='Второй собеседник')

    class Meta:
        verbose_name = 'диалог'
        verbose_name_plural = 'диалоги'

    def __str__(self):
        return f'диалог между {self.first_participant} и {self.second_participant}'


class Message(BaseModel):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, verbose_name='Диалог')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', verbose_name='Отправитель')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', verbose_name='Получатель')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    text = models.TextField(verbose_name='Сообщение')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return self.text


class FAQ(BaseModel):
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    class Meta:
        verbose_name = 'Вопрос и ответ'
        verbose_name_plural = 'Вопросы и ответы'

    def __str__(self):
        return f'{self.question} -- {self.answer}'

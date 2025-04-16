import datetime
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from events.models import Event, Participation, Favorite, Category
from django.urls import reverse

User = get_user_model()


class EventModelTest(TestCase):
    def setUp(self):
        # Создаём пользователя и категорию
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name="Конференция")
        # Создаём событие
        self.event = Event.objects.create(
            title="Тестовое мероприятие",
            description="Описание тестового мероприятия",
            date=timezone.now() + datetime.timedelta(days=1),
            location="Минск",
            organizer=self.user,
            participant_limit=2
        )
        self.event.categories.add(self.category)

    def test_str_method(self):
        # Проверяем, что метод __str__ возвращает название события
        self.assertEqual(str(self.event), "Тестовое мероприятие")

    def test_is_not_finished_by_default(self):
        # В новом событии поле is_finished должно быть False
        self.assertFalse(self.event.is_finished)


class ParticipationModelTest(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(username='organizer', password='password')
        self.participant = User.objects.create_user(username='participant', password='password')
        self.event = Event.objects.create(
            title="Мероприятие для участия",
            description="Проверка участия",
            date=timezone.now() + datetime.timedelta(days=1),
            location="Брест",
            organizer=self.organizer,
            participant_limit=2,
        )

    def test_registration(self):
        # Проверяем, что можно корректно создать объект участия
        participation = Participation.objects.create(user=self.participant, event=self.event, status='registered')
        self.assertEqual(participation.status, 'registered')


class FavoriteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='favuser', password='password')
        self.organizer = User.objects.create_user(username='organizer', password='password')
        self.event = Event.objects.create(
            title="Избранное мероприятие",
            description="Проверка избранного",
            date=timezone.now() + datetime.timedelta(days=1),
            location="Гомель",
            organizer=self.organizer,
            participant_limit=5,
        )

    def test_add_to_favorite(self):
        # Добавляем событие в избранное
        Favorite.objects.create(user=self.user, event=self.event)
        self.assertTrue(Favorite.objects.filter(user=self.user, event=self.event).exists())


class EventViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = 'password'
        # Создаем организатора и обычного пользователя
        self.organizer = User.objects.create_user(username='organizer', password=self.password)
        self.user = User.objects.create_user(username='regular', password=self.password)

        # Создаем категорию и событие
        self.category = Category.objects.create(name="Семинар")
        self.event = Event.objects.create(
            title="Тестовое мероприятие",
            description="Детальное описание.",
            date=timezone.now() + datetime.timedelta(days=1),
            location="Минск",
            organizer=self.organizer,
            participant_limit=2,
        )
        self.event.categories.add(self.category)

    def test_event_list_view(self):
        # Проверяем, что страница списка мероприятий загружается и содержит название нашего события
        url = reverse('event_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)

    def test_event_detail_view(self):
        # Проверяем детальную страницу события
        url = reverse('event_detail', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)
        self.assertContains(response, self.event.description)


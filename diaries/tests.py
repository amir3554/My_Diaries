from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Diary

User = get_user_model()

class DiaryDeleteTest(TestCase):
    
    def setUp(self):

        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        self.diary = Diary.objects.create(
            title='title1',
            description='desc1',
            user= self.user1 
        )

        self.client = Client()

    def test_owner_can_delete_diary(self):

        self.client.login(username='user1', password="pass123")

        response = self.client.delete(reverse('DeleteDiary', kwargs={'pk' : self.diary.pk}),
            {
                'diary' : self.diary.pk
            }
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Diary.objects.filter(pk=self.diary.pk).exists())

    def test_other_user_cannot_delete_diary(self):
        # تسجيل دخول user2
        self.client.login(username='user2', password='pass123')

        response = self.client.delete(reverse('DeleteDiary', kwargs={'pk': self.diary.pk}), {
            'diary': self.diary.pk
        })

        self.assertEqual(response.status_code, 403)  # لا يملك الصلاحية
        self.assertTrue(Diary.objects.filter(pk=self.diary.pk).exists())
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile


class ProfileViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="test11", password="1")
        cls.profile = Profile.objects.create(email='dvl@inbox.ru', fullName='Gigs', phone='86579875645', user_id=1)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.profile.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_sign_up(self):
        data = json.dumps({"username": 'test12',
                           "password": '123',
                           "name": "george",
                           "email": "dvyl@inbox.ru",
                           "phone": "89117576841", })
        response = self.client.post(reverse("myauth:sign-up"), data=data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_sign_up_false(self):
        data = json.dumps({"username": 'test12',
                           "password": '123',
                           "name": "george",
                           "email": "dvylinbox.ru",
                           "phone": "89117576841", })
        response = self.client.post(reverse("myauth:sign-up"), data=data,
                                    content_type='application/json')

        self.assertEqual(str(response.data['email']),
                         "[ErrorDetail(string='Enter a valid email address.', code='invalid')]")

        self.assertEqual(response.status_code, 400)

    def test_sign_in(self):
        data = json.dumps({"username": 'test11',
                           "password": '1',
                           })
        response = self.client.post(reverse("myauth:sign-in"), data=data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_profile_edit_post(self):
        data = json.dumps({"fullName": 'George',
                           "phone": '86573243454',
                           'email': "re@inbox.ru",
                           })
        response = self.client.post(reverse("myauth:profile_edit"), data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_profile_edit_post_false(self):
        data = json.dumps({"fullName": 'George',
                           "phone": '86573243454',
                           'email': "reinboxru",
                           })
        response = self.client.post(reverse("myauth:profile_edit"), data,
                                    content_type='application/json')

        self.assertEqual(str(response.data['email']),
                         "[ErrorDetail(string='Enter a valid email address.', code='invalid')]")
        self.assertEqual(response.status_code, 400)

    def test_profile_edit_get(self):

        response = self.client.get(reverse("myauth:profile_edit"))

        profile = Profile.objects.all()[0]

        self.assertEqual(response.status_code, 200)

        self.assertEqual(profile.email, self.profile.email)

    def test_profile_images(self):
        image_content = b'Image content'

        data = {"avatar": SimpleUploadedFile('test_image.jpg',
                                             image_content, content_type='image/jpeg')}
        response = self.client.post(reverse("myauth:profile_avatar"), data=data)

        db_instance = Profile.objects.all()[0]

        self.assertEqual(response.status_code, 200)

        self.assertEqual(db_instance.src.url[:27], '/media/avatar_1/test_image_')

    def test_profile_password(self):

        data = {'passwordCurrent': '1',
                'password': '2',
                'passwordReply': '2'}

        response = self.client.post(reverse("myauth:profile_pass"), data=data, content_type='application/json')

        user = User.objects.all()[0]
        result_password = data['password']

        self.assertEqual(response.status_code, 200)

        self.assertTrue(user.check_password(int(result_password)))

    def test_profile_password_false(self):

        data = {'passwordCurrent': '3',
                'password': '2',
                'passwordReply': '2'}

        response = self.client.post(reverse("myauth:profile_pass"), data=data, content_type='application/json')

        user = User.objects.all()[0]
        result_password = data['password']

        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.data['message'], 'the password does not match')

        self.assertFalse(user.check_password(int(result_password)))

    def test_sign_out(self):
        response = self.client.post(reverse("myauth:sign-out"))

        self.assertEqual(response.status_code, 200)


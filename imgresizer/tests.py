from django.test import TestCase
from django.urls import reverse
from .models import Images
from .forms import UploadForm, ResizeForm, get_clear_url
from .views import get_file_name_from_url, get_format_for_PIL, resize_image
  

class IndexViewTests(TestCase):

    def test_no_images(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Нет доступных изображений')
        self.assertQuerysetEqual(response.context['images'], [])

    def test_one_image_object(self):
        Images.objects.create(name='default.jpg', imgblob='base64_image_representation')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['images'], ['<Images: default.jpg>'])

    def test_many_image_objects(self):
        Images.objects.create(name='1.jpg', imgblob='base64_image_representation')
        Images.objects.create(name='2.jpg', imgblob='base64_image_representation')
        Images.objects.create(name='3.jpg', imgblob='base64_image_representation')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['images'], ['<Images: 1.jpg>', '<Images: 2.jpg>', '<Images: 3.jpg>'], ordered=False)

class UploadViewTests(TestCase):

    def test_upload_view_availability(self):
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UploadForm)

class ResizeViewTests(TestCase):

    def test_resize_view_availability_for_true_img_id(self):
        obj = Images.objects.create(name='default.jpg', imgblob='base64_image_representation')
        response = self.client.get(reverse('resize', kwargs={'img_id':obj.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['img_obj'], Images)
        self.assertIsInstance(response.context['form'], ResizeForm)

    def test_resize_view_availability_for_false_img_id(self):
        obj_id = 999999
        response = self.client.get(reverse('resize', kwargs={'img_id':obj_id}))
        self.assertEqual(response.status_code, 404)

class SupportingFunctionsTests(TestCase):

    def test_get_clear_url(self):
        url = 'https://www.site.com/asd/fgh/image.jpg?a=5&b=foo&c=?bar'
        self.assertEqual(get_clear_url(url), 'https://www.site.com/asd/fgh/image.jpg')

    def test_get_file_name_from_url(self):
        url = 'https://www.site.com/asd/fgh/image.jpg'
        self.assertEqual(get_file_name_from_url(url), 'image.jpg')

    def test_get_format_for_PIL(self):
        file_name = 'image.png'
        self.assertEqual(get_format_for_PIL(file_name), 'png')
        file_name = 'image.jpeg'
        self.assertEqual(get_format_for_PIL(file_name), 'jpeg')
        file_name = 'image.jpg'
        self.assertEqual(get_format_for_PIL(file_name), 'jpeg')

    def test_resize_image(self):
        imgblob = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P//PwAGBAL/VJiKjgAAAABJRU5ErkJggg=='
        obj = Images.objects.create(name='image.png', imgblob=imgblob)
        self.assertIsInstance(resize_image(obj, 100, 100), Images)

class UploadFormTest(TestCase):
    pass
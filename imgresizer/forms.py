from django import forms
from django.core.exceptions import ValidationError
import mimetypes
import requests


def get_clear_url(url):
    # очистим ссылку от возможного наличия параметров
    return url[:url.find('?')] if url.find('?') > 0 else url

def validate_mimetype(url):
    # используя mime type объекта удостоверимся, что это изображение
    url = get_clear_url(url)
    mimetype, _ = mimetypes.guess_type(url)
    print(mimetype)
    if mimetype:
        if not mimetype.startswith('image'):
            raise ValidationError('Не найдено изображение по ссылке')
    else:
        raise ValidationError('Не найдено изображение по ссылке')

def is_url_exist(url):
    try:
        response = requests.get(url) # при несуществующем домене возникает ошибка
    except:
        raise ValidationError(c'Ссылка не существует')
    if not response.status_code == 200: # домен существует, но не найден сам ресурс
        raise ValidationError('Ссылка не существует')
    if url != response.url: # редирект?
        raise ValidationError('Похоже, что ссылка не существует!')

class UploadForm(forms.Form):

    url = forms.URLField(label='Ссылка', required=False)
    file = forms.ImageField(label='Файл', required=False)

    def clean(self):
        cleaned_data = super().clean()
        url = get_clear_url(cleaned_data.get('url'))
        cleaned_data['url'] = url
        file = cleaned_data.get('file')

        if url and file:
            raise ValidationError('Только одно поле должно быть заполнено')

        if url:
            is_url_exist(url)
            validate_mimetype(url)

        if not url and not file:
            raise ValidationError('Укажите url или загрузите файл')


class ResizeForm(forms.Form):

    height = forms.IntegerField(min_value=1, max_value=2000, label='Высота', required=False)
    width = forms.IntegerField(min_value=1, max_value=2000, label='Ширина', required=False)

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get('height')
        width = cleaned_data.get('width')

        if not height and not width:
            raise ValidationError('Введите хотя бы одно значение')
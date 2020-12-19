from django import forms
from django.core.exceptions import ValidationError
import mimetypes


def get_clear_url(url):
    # очистим ссылку от возможного наличия параметров
    return url[:url.find('?')] if url.find('?') > 0 else url

def validate_mimetype(url):
    # используя mime type объекта удостоверимся, что это изображение
    url = get_clear_url(url)
    mimetype, _ = mimetypes.guess_type(url)

    if mimetype:
        if not mimetype.startswith('image'):
            raise ValidationError('Не найдено изображение по ссылке')
    else:
        raise ValidationError('Не найдено изображение по ссылке')


class UploadForm(forms.Form):

    url = forms.URLField(label='Ссылка', required=False, validators=[validate_mimetype])
    file = forms.ImageField(label='Файл', required=False)

    def clean(self):
        #raise ValidationError('Валидация олоололо азазазаза')
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        cleaned_data['url'] = get_clear_url(url)
        file = cleaned_data.get('file')

        if url and file:
            raise ValidationError('Только одно поле должно быть заполнено')

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
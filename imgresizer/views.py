from django.shortcuts import render, get_object_or_404, redirect
from .forms import UploadForm, ResizeForm
from .models import Images
import base64
import requests
from io import BytesIO
from PIL import Image as PILImage # что бы визуально не перепутать с моделью Images

# ----------------------------
# --- SUPPORTING FUNCTIONS ---
# ----------------------------

def get_format_for_PIL(name):
    format_ = ''
    pos = name.rfind('.')
    if pos > 0:
        format_ = name[pos+1:]
    if format_.lower() == 'jpg': # не поддерживается
        format_ = 'jpeg'
    return format_

def resize_image(obj, width, height):
    img = PILImage.open(BytesIO(base64.b64decode(obj.imgblob)))
    if not width:
        width = 9999
    if not height:
        height = 9999
    width_old, height_old = img.size # старые размеры изображения
    resize_ratio = min(width/width_old, height/height_old) # для сохранения пропорций
    img_resized = img.resize(size=(int(width_old*resize_ratio), int(height_old*resize_ratio))) # меняем размер изображения
    buffered = BytesIO()
    format_ = get_format_for_PIL(obj.name) # получаем необходимый формат для последующего преобразования данных изображения
    img_resized.save(buffered, format=format_)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return Images(name=obj.name ,imgblob=img_str)

def get_file_name_from_url(url):
    fpos = url.rfind('/')
    lpos = len(url)
    file_name = url[fpos+1:lpos] # вытаскиваем название файла из урл
    return file_name

# -----------------------
# --- VIEWS FUNCTIONS ---
# -----------------------

def index(request):
    context = {}
    image_objs = Images.objects.all() # получаем все объекты изображений из бд
    context['images'] = image_objs # передаем их в контекст
    return render(request, 'imgresizer/index.html', context)

def upload(request):
    context = {}
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data.get('url')
            file = form.cleaned_data.get('file')

            if file: # если загружен файл с локальной машины
                file_name = file.name
                imgblob = base64.b64encode(file.read()).decode() # читаем файл, кодируем в base64, меняем байтовый тип получившейся строки на строковый
            elif url: # если указана ссылка на изображение
                file_name = get_file_name_from_url(url) # вытаскиваем название файла из урл
                r = requests.get(url)
                imgblob = base64.b64encode(r.content).decode() # получаем изображение в base64

            obj = Images.objects.create(name = file_name, imgblob = imgblob)
            
            return redirect('resize', img_id=obj.id)

    else:
        form = UploadForm()

    context['form'] = form

    return render(request, 'imgresizer/upload.html', context)

def resize(request, img_id):

    context = {}

    obj = get_object_or_404(Images, id=img_id)

    if request.method == 'POST':
        form = ResizeForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')
            obj = resize_image(obj, width, height)
    else:
        form = ResizeForm()

    context['img_obj'] = obj
    context['form'] = form

    return render(request, 'imgresizer/resize.html', context)
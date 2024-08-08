from django.urls import path

from . import views

urlpatterns = [
    # Если вызван URL без относительного адреса (шаблон — пустые кавычки),
    # то вызывается view-функция main_page() из файла views.py
    path('', views.main_page),
    path('view', views.view_page),
    path('<name>', views.paste_page),
    path('<name>/raw', views.raw_page)
]

from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<int:category_id>/',views.post_by_category,name='post_by_category'),
]

"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import chat
from .views import show_user_queries
from .views import LogView
from .views import editable_dashboard


urlpatterns = [
    url(r'^chat/$', chat, name='chat'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/dashboard/', show_user_queries, name='display'),
    # url(r'^dashboard/', LogView.as_view(), name='bdisplay'),
    url(r'^update/', editable_dashboard, name='bdisplay'),
    url(r'^dashboard/', editable_dashboard, name='bdisplay'),

]



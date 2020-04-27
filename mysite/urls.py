"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app01/', include("app01.urls")),  # 图书管理APP

    url(r'^login/', views.login),  # 登录页面
    url(r'^index/', views.index),  # 主页面

    # 删除功能三合一
    url(r'^delete_(press|book|author)/(\d+)/', views.delete),  # 删除出版社

    # --------------出版社相关的 ↓ -------------------
    url(r'^press_list/', views.press_list, name='press'),  # 展示出版社页面
    url(r'^add_press/', views.add_press),  # 添加出版社
    # url(r'^add_press/', views.AddPress.as_view()),  # 添加出版社, 固定写法
    url(r'^delete_press/(\d+)/', views.delete_press),  # 删除出版社
    url(r'^edit_press/', views.edit_press),  # 编辑出版社

    # ---------------书相关的 ↓-----------------------
    url(r'^book_list/', views.book_list, name='book'),  # 展示书的列表
    url(r'^add_book/', views.add_book),  # 添加书
    url(r'^delete_book/(\d+)', views.delete_book),  # 删除书
    url(r'^edit_book/', views.edit_book),  # 编辑书

    # ---------------作者相关的 ↓-----------------------
    url(r'^author_list/', views.author_list, name='author'),  # 展示作者的列表
    url(r'^add_author/', views.add_author),  # 添加作者
    url(r'^delete_author/(\d+)', views.delete_author),  # 删除作者
    url(r'^edit_author/', views.edit_author),  # 编辑书

    url(r'^upload/', views.upload),  # 上传文件

]

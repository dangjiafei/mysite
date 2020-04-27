from django.conf.urls import url
from app01 import views

urlpatterns = [

    url(r'^login/', views.login),  # 登录页面
    url(r'^index/', views.index),  # 主页面

    # --------------出版社相关的 ↓ -------------------
    # 展示出版社页面, name="press"这个参数的作用是可以在其他地方引用的时候写入这个, 想修改的时候直接改路由就可以了
    url(r'^press_list/', views.press_list, name="press"),
    url(r'^add_press/', views.add_press),  # 添加出版社
    # url(r'^add_press/', views.AddPress.as_view()),  # 添加出版社, 固定写法
    url(r'^delete_press/(\d+)/', views.delete_press),  # 删除出版社
    url(r'^edit_press/', views.edit_press),  # 编辑出版社

    # ---------------书相关的 ↓-----------------------
    url(r'^book_list/', views.book_list),  # 展示书的列表
    url(r'^add_book/', views.add_book),  # 添加书
    url(r'^delete_book/(\d+)', views.delete_book),  # 删除书
    url(r'^edit_book/', views.edit_book),  # 编辑书

    # ---------------作者相关的 ↓-----------------------
    url(r'^author_list/', views.author_list),  # 展示作者的列表
    url(r'^add_author/', views.add_author),  # 添加作者
    url(r'^delete_author/(\d+)', views.delete_author),  # 删除作者
    url(r'^edit_author/', views.edit_author),  # 编辑书

    url(r'^upload/', views.upload),  # 上传文件

]

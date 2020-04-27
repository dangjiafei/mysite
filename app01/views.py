# render表示可以返回html文件, HttpResponse表示返回文本信息, redirect表示跳转至其他页面地址
import os
import time
from django.shortcuts import HttpResponse, redirect, render, reverse
from app01 import models
from mysite import settings
from django.views import View
from django.utils.decorators import method_decorator  # 这是用于装饰器的  用法：@method_decorator(timer)


def login(request):
    error_msg = ''
    # 需要判断
    if request.method == "POST":
        # 如果是第二次来，表单填写完成要给我发送数据
        # 拿到用户发过来的数据
        email = request.POST.get("email")
        pwd = request.POST.get("pwd")
        # 从数据库查询有没有这个用户
        res = models.User.objects.filter(email=email, pwd=pwd)
        print(res)
        if res:
            # 登录成功
            return redirect("/index/")
        else:
            # 登录失败，提示用户邮箱或密码错误
            error_msg = "邮箱或密码错误"
    # 如果是第一次来，是跟我要一个登录页面用来填写数据
    return render(request, "login.html", {"error_msg": error_msg})


def index(request):
    return render(request, "index.html")


# 出版社列表展示函数
def press_list(request):
    # 去数据库查所有的出版社
    res = models.Press.objects.all().order_by('id')  # 按照id排序显示
    # 在HTML页面上显示出来
    return render(request, "press_list.html", {"res": res})


# 添加出版社
def add_press(request):
    add_error_msg = ''
    if request.method == "POST":
        if request.POST.get("name"):
            # 表示用户填写完成，要给我发数据
            # 1、取到用户填写的出版社数据
            press_name = request.POST.get("name")
            # 2、将数据添加到数据库中
            models.Press.objects.create(name=press_name)
            # 3、跳转到出版社列表页面
            return redirect('/press_list/')
        else:
            add_error_msg = "出版社名称不能为空"
            return render(request, "add_press.html", {"add_error_msg": add_error_msg})

    return render(request, "add_press.html", {"add_error_msg": add_error_msg})


# 时间装饰器
def timer(fn):
    def inner(*args, **kwargs):
        start_time = time.time()
        res = fn(*args, **kwargs)
        print("函数执行时间为{}".format(time.time() - start_time))
        return res

    return inner


# 添加出版社类
class AddPress(View):

    @method_decorator(timer)  # 在执行get、post请求的时候都会有装饰器的效果，因为dispatch方法在里面会自动执行
    def dispatch(self, request, *args, **kwargs):
        print("执行之前")
        res = super().dispatch(request, *args, **kwargs)
        print("执行之后")
        return res

    def get(self, request):
        add_error_msg = ''
        return render(request, "add_press.html", {"add_error_msg": add_error_msg})

    def post(self, request):
        add_error_msg = ''
        if request.POST.get("name"):
            # 表示用户填写完成，要给我发数据
            # 1、取到用户填写的出版社数据
            press_name = request.POST.get("name")
            # 2、将数据添加到数据库中
            models.Press.objects.create(name=press_name)
            # 3、跳转到出版社列表页面
            return redirect('/press_list/')
        else:
            add_error_msg = "出版社名称不能为空"
            return render(request, "add_press.html", {"add_error_msg": add_error_msg})


# 删除出版社
def delete_press(request, delete_id):
    # 1、获取要删除的出版社id
    # delete_id = request.GET.get("id")
    # 2、根据id去数据库删除对应的数据行
    models.Press.objects.filter(id=delete_id).delete()
    # 3、让用户再去访问一下出版社列表页
    return render(request, "delete_press.html")


# 编辑出版社  利用request.GET.get('id'), 直接在URL中拿到要修改的id
def edit_press(request):
    # 1、获取要编辑的出版社id
    edit_id = request.GET.get('id')

    if request.method == "POST":
        # 用户修改完出版社的数据给我返回
        # 1、取出用户编辑之后的数据
        new_name = request.POST.get("name")
        # 2、去数据库中修改对应的数据
        # 2.1 先找到对应的数据
        edit_press_obj = models.Press.objects.get(id=edit_id)
        edit_press_obj.name = new_name  # 只是在ORM中修改了数据，还没有同步到数据库
        # 2.3 将修改过的数据同步到数据库中
        edit_press_obj.save()
        # 3、让用户再去访问出版社列表页
        return redirect("/press_list/")

    # 2、获取该出版社的信息
    # res = Press.objects.filter(id=edit_id)[0]  # filter返回的是一个列表, 加上索引[0]就可以获取目标对象，推荐用这个，拿不到不会报错
    res = models.Press.objects.get(id=edit_id)  # get有且只能找到一个对象，否则就报错
    # 3、在页面上展示出来
    return render(request, "edit_press.html", {"press_obj": res})


# 书籍列表展示函数
def book_list(request):
    # 1、查询所有的书籍数据
    data = models.Book.objects.all()
    # 2、在页面上展示, 返回完整的HTML页面
    return render(request, 'book_list.html', {'data': data})


# 添加书
def add_book(request):
    add_error_msg = ''

    # 获取出版社的信息
    press_data_list = models.Press.objects.all().order_by('id')

    if request.method == "POST":
        if request.POST.get("book_name"):
            # 表示用户填写完成，要给我发数据
            # 1、取到用户填写的书名称数据
            book_name = request.POST.get("book_name")
            # 书的价格
            book_price = request.POST.get("book_price")
            # 对应的出版社id
            press_id = request.POST.get("press_id")
            # 2、将数据添加到数据库中

            # 基于外键对象的创建, 注意：press=press_obj是传入的对象, press在数据库中是对象
            # press_obj = Press.objects.get(id=press_id)
            # Book.objects.create(title=book_name, press=press_obj)

            # 基于外键id值的创建
            models.Book.objects.create(title=book_name, press_id=press_id, price=book_price)
            # 3、跳转到书列表页面
            return redirect('/book_list/')
        else:
            add_error_msg = "书名称不能为空"
            return render(
                request, "add_book.html",
                {"add_error_msg": add_error_msg, "press_data_list": press_data_list})

    return render(
        request,
        "add_book.html",
        {"add_error_msg": add_error_msg, "press_data_list": press_data_list})


# 删除书
def delete_book(request, delete_book_id):
    # 1、获取要删除的书id
    # delete_book_id = request.GET.get("id")
    # 2、根据id去数据库删除对应的数据行
    models.Book.objects.filter(id=delete_book_id).delete()
    # 3、让用户再去访问一下书列表页
    return render(request, "delete_book.html")


# 编辑书
def edit_book(request):
    # 1、获取要编辑的书id
    edit_id = request.GET.get('id')

    # 2、去数据库中修改对应的数据
    edit_book_obj = models.Book.objects.get(id=edit_id)

    press_data = models.Press.objects.all()

    if request.method == "POST":
        # 获取修改书对应的出版社
        new_press_id = request.POST.get("press_id")

        # 用户修改完书的数据给我返回
        # 1、取出用户编辑之后的数据
        new_title = request.POST.get("name")
        edit_book_obj.title = new_title  # 只是在ORM中修改了数据，还没有同步到数据库
        edit_book_obj.press_id = new_press_id
        # 2、将修改过的数据同步到数据库中
        edit_book_obj.save()
        # 3、让用户再去访问书列表页
        return redirect("/book_list/")

    # 3、在页面上展示出来
    return render(request, "edit_book.html", {"book_obj": edit_book_obj, "press_data": press_data})


# 作者列表展示函数
def author_list(request):
    # 1、去数据库中查询所有的作者
    author_data = models.Author.objects.all()
    # for author in author_data:
    # print(author.books)  # 这个事ORM提供的桥梁，只能拿到对应的对象，要想获得值，还需要往后找
    # print(author.books.all())  # 这个可以拿到作者名下对应的书
    # 2、在页面上展示
    return render(request, "author_list.html", {"author_list": author_data})


# 添加作者
def add_author(request):
    add_error_msg = ''
    # 获取所有的书籍信息
    book_data = models.Book.objects.all()
    if request.method == "POST":
        if request.POST.get("author_name"):
            # 1、取到用户填写的信息
            new_author_name = request.POST.get("author_name")
            book_ids = request.POST.getlist("books")
            # 2、添加到数据库
            # 2.1 创建新的作者
            author_obj = models.Author.objects.create(name=new_author_name)
            # 2.2 创建作者和书的对应关系
            author_obj.books.add(*book_ids)  # 参数是一个一个单独的书籍id值
            # author_obj.books.set(book_ids)  # 参数是一个列表所有书籍id值
            return redirect('/author_list/')
        else:
            add_error_msg = "姓名不能为空"
            return render(
                request, "add_author.html",
                {"add_error_msg": add_error_msg, "book_list": book_data})
    # 返回一个页面给用户，让用户填写作者信息
    return render(
        request, "add_author.html",
        {"add_error_msg": add_error_msg, "book_list": book_data})


# 删除作者
def delete_author(request, delete_author_id):
    # 1、获取要删除的作者id
    # delete_author_id = request.GET.get("id")
    # 2、根据id去数据库删除对应的数据行
    models.Author.objects.filter(id=delete_author_id).delete()
    # 3、让用户再去访问一下书列表页
    return render(request, "delete_author.html")


# 编辑作者
def edit_author(request):
    # 1、取到要编辑的作者id值
    edit_author_id = request.GET.get("id")
    # 2、找到要编辑的对象
    edit_author_obj = models.Author.objects.get(id=edit_author_id)
    if request.method == "POST":
        # 拿到编辑之后的数据
        new_author_name = request.POST.get("author_name")
        new_book_ids = request.POST.getlist("book_ids")

        # 去数据库修改作者表
        edit_author_obj.name = new_author_name
        edit_author_obj.save()

        # 去数据库修改作者和书的关系表
        edit_author_obj.books.set(new_book_ids)  # set方法是一个列表
        # edit_author_obj.books.add(*new_book_ids)  # add方法是接受一个一个的参数, 因此需要拆包

        # 跳转至作者列表页
        return redirect("/author_list/")

    # 2.1 找到所有的书籍对象
    book_data = models.Book.objects.all()
    # 3、返回一个页面
    return render(request, "edit_author.html", {"author_obj": edit_author_obj, "book_list": book_data})


# 上传文件
def upload(request):
    if request.method == "POST":
        file_obj = request.FILES.get("file_name")
        file_name = file_obj.name  # 拿到文件对象，可以通过(.name)属性拿到文件名
        # 判断当前是否存在该文件
        if os.path.exists(os.path.join(settings.BASE_DIR, file_name)):
            name, suffix = file_name.split(".")
            name += "2"
            file_name = name + "." + suffix
        # 从上传文件对象中，一点一点读取数据
        with open(file_name, "wb") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
            return HttpResponse("上传完成")
    # 返回给用户一个界面，用于选择文件
    return render(request, "upload.html")


# 删除功能三合一
def delete(request, table, del_id):
    """
    :param request:
    :param table: 传过来的book|author|press中的其中一个
    :param del_id: 传过来要删除的id
    :return:
    """
    print(table)
    print(del_id)
    table_obj = getattr(models, table.capitalize())
    table_obj.objects.get(id=del_id).delete()
    return redirect(reverse(table))

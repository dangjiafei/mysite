from django.db import models


# 用户
class User(models.Model):
    id = models.AutoField(primary_key=True)  # 创建一个自增的ID列作为主键
    email = models.CharField(max_length=32)  # varchar(32)
    pwd = models.CharField(max_length=32)  # varchar(32)

    def __str__(self):
        return self.email


# 出版社
class Press(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


# 书
class Book(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    title = models.CharField(max_length=32)  # 书名
    price = models.IntegerField()  # 书的价格
    # 在Django2.0之后必须指定on_delete参数，Django 1.11默认就是级联删除
    # to=关联的表名，加引号是因为有的类写在后面，可以通过映射
    press = models.ForeignKey(to='Press', on_delete=models.CASCADE)  # 外键关联

    def __str__(self):
        return self.title


# 作者
class Author(models.Model):
    id = models.AutoField(primary_key=True)  # 自增id主键
    name = models.CharField(max_length=32)  # 作者名字
    books = models.ManyToManyField(to='Book')  # 数据库中没有这个字段，这个只是ORM层面建立的一个多对多的关系

    def __str__(self):
        return self.name

# 创建作者和书籍的关系表(可以用Django中内置的ManyToManyField进行多对多的关联)
# class Author2Book(models.Model):
#     id = models.AutoField(primary_key=True)  # 自增id主键
#     author_id = models.ForeignKey(to='Author', on_delete=models.CASCADE)  # 作者id
#     book_id = models.ForeignKey(to='Book', on_delete=models.CASCADE)  # 书id

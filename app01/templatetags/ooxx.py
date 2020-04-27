# -*- coding: utf-8 -*-
# @Time     : 2020/3/31 23:03
# @Author   : Dang_Jiafei
# @Email    : 18840341320@163.com
from django import template

# 固定写法，生成一个注册实例对象
register = template.Library()


# name参数可以用来弄别名，不设置就是方法本身名，可选参数
@register.filter(name="add_str_md")  # 告诉Django的模板语言，我现在注册注册一个自定义的filter
def add_str_md(value, arg):
    """
    给任意指定的变量添加str字符串
    :param value: |左边被修饰的那个变量
    :param arg: 参数只能是一个
    :return: 修改后的变量内容
    """
    return value + arg


# 在自定义完成之后，要是想使用，还需要在HTML中进行加载模块，实例：{% load ooxx %}
# 模板语言使用规则{{ obj|method:arg }} obj表示要操作的对象，method表示要执行的方法，args表示参数，3个值中间不能有空格


# 自定义simple_tag, 和自定义filter类似, 只不过接收更灵活的参数
@register.simple_tag
def join_str(*args, **kwargs):
    return '-'.join(args)


# 用法：一样需要{% load ooxx %}, <h1>{% join_str 'alex' 'is' 'nb' key1='hh' key2='xx' %}</h1>


# 返回HTMl页面(多用于返回html代码片段)
@register.inclusion_tag("pagination.html")
def pagination(total, current_num):
    return {'total': range(1, total + 1), 'current_num': current_num}

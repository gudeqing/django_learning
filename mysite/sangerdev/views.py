# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .models import WebAPI, Arg
import os
from jinja2 import Environment
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    last_one = WebAPI.objects.last()
    api_name_id = last_one.id
    api_name = last_one.api_name
    package_rel_path = last_one.package_rel_path
    description = last_one.description
    option_list = Arg.objects.filter(api_name_id=api_name_id).values()
    new_option_list = list()
    for tmp_dict in option_list:
        new_dict = dict()
        for key, value in tmp_dict.items():
            if key in ["arg_name", "arg_type", "arg_default", "arg_format"]:
                new_dict[key[4:]] = value
        new_option_list.append(new_dict)

    # format python code
    env = Environment()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tool_template_file = base_dir +'/templates/sangerdev/tool_template.jinja2'
    print(tool_template_file)
    tool_template = env.from_string(open(tool_template_file).read())
    tool_code = tool_template.render(
        raw_tool_name=api_name.split(".")[-1],
        tool_name=''.join(x.capitalize() for x in api_name.split("_")),
        tool_path=api_name,
        package_rel_path=package_rel_path,
        called_script='_'.join(package_rel_path.split("/")[-1].split(".")[:-1]),
        option_list=new_option_list,
        tool_description=description,
    )
    tool_code2html = highlight(tool_code, PythonLexer(), HtmlFormatter())
    # format css file for python code
    css_file = base_dir + '/static/sangerdev/python_code_style.css'
    if os.path.exists(css_file):
        pass
    else:
        with open(css_file, 'w', encoding="utf-8") as f:
            css_code = HtmlFormatter().get_style_defs('.highlight')
            f.write(css_code)
    # render
    data = dict(python_code=tool_code2html, )
    return render(request, 'sangerdev/index.html', data)

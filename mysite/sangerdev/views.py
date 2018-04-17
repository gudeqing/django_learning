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
    get_info = request.GET
    if not request.GET:
        select_one = WebAPI.objects.last()
        which_template = "tool"
        which_api = select_one.api_name
    else:
        select_one = WebAPI.objects.filter(id=get_info['which_api'])[0]
        which_template = get_info['which_template']
        which_api = select_one.api_name
    api_name_id = select_one.id
    api_name = select_one.api_name
    package_rel_path = select_one.package_rel_path
    controller = select_one.controller
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
    # format css file for python code
    css_file = base_dir + '/static/sangerdev/python_code_style.css'
    if os.path.exists(css_file):
        pass
    else:
        with open(css_file,'w',encoding="utf-8") as f:
            css_code = HtmlFormatter().get_style_defs('.highlight')
            f.write(css_code)

    # format python code for tool
    if get_info and get_info['which_template'] == "tool":
        tool_template_file = base_dir +'/templates/sangerdev/tool_template.jinja2'
        print(tool_template_file)
        tool_template = env.from_string(open(tool_template_file, encoding="utf-8").read())
        tool_code = tool_template.render(
            tool_path=api_name,
            raw_tool_name=api_name.split(".")[-1],
            tool_name=''.join(x.capitalize() for x in api_name.split(".")[-1].split("_")),
            package_rel_path=package_rel_path.replace(".", "/"),
            called_script=package_rel_path.split(".")[-1],
            option_list=new_option_list,
        )
        python_code = highlight(tool_code, PythonLexer(), HtmlFormatter())
    elif get_info and get_info['which_template'] == "web_api":
        template_file = base_dir + '/templates/sangerdev/webapi_template.jinja2'
        print("web_api_template:", template_file)
        template = env.from_string(open(template_file, encoding="utf-8").read())
        tool_code = template.render(
            raw_tool_name=api_name.split(".")[-1],
            tool_name=''.join(x.capitalize() for x in api_name.split(".")[-1].split("_")),
            option_list=new_option_list,
            controller=controller,
            controller_class = ''.join(x.capitalize() for x in controller.split("_")),
            to_file_path = controller.split("_controller")[0]
        )
        python_code = highlight(tool_code, PythonLexer(), HtmlFormatter())
    elif get_info and get_info['which_template'] == "db_api":
        template_file = base_dir + '/templates/sangerdev/dbapi_template.jinja2'
        template = env.from_string(open(template_file, encoding="utf-8").read())
        tool_code = template.render(
            raw_tool_name=api_name.split(".")[-1],
            tool_name=''.join(x.capitalize() for x in api_name.split(".")[-1].split("_")),
        )
        python_code = highlight(tool_code, PythonLexer(), HtmlFormatter())
    elif get_info and get_info['which_template'] == "workflow":
        template_file = base_dir + '/templates/sangerdev/workflow_template.jinja2'
        template = env.from_string(open(template_file, encoding="utf-8").read())
        tool_code = template.render(
            raw_tool_name=api_name.split(".")[-1],
            tool_name=''.join(x.capitalize() for x in api_name.split(".")[-1].split("_")),
            project_type=controller.split("_controller")[0],
            option_list=new_option_list,
        )
        python_code = highlight(tool_code, PythonLexer(), HtmlFormatter())
    else:
        python_code = """
        <h2>step1: Login and set options</h2>
        <h2>step2: Select Options Above</h2>
        <h2>step3: Check the code and modified it</h2>
        """
        tool_code = "None"

    # save code
    code_path = base_dir + '/static/sangerdev/' + api_name.split(".")[-1] + '.py'
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(tool_code+'/n')
    print(code_path)
    # render
    data = dict(
        python_code=python_code,
        all_api_names=WebAPI.objects.all(),
        raw_python_code=tool_code,
        template_types=["tool", "web_api", "workflow", "db_api"],
        which_api=which_api,
        which_template=which_template,
        code_path=request.path + api_name.split('.')[-1] + '.py',
        raw_tool_name=api_name.split(".")[-1],
    )
    # print(request.get_full_path())
    from django.contrib import admin
    print("admin:",admin.site.urls)
    return render(request, 'sangerdev/index.html', data)



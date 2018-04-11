from django.shortcuts import render
from django.http import HttpResponse
from .models import WebAPI, Arg


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    last_one = WebAPI.objects.last()
    api_name_id = last_one.id
    api_name = last_one.api_name
    package_rel_path = last_one.package_rel_path
    description = last_one.description
    option_list = Arg.objects.filter(api_name_id=api_name_id).values()
    data = dict(
        tool_name=api_name,
        raw_tool_name=''.join(x.capitalize() for x in api_name.split("_")),
        tool_parent_dir="",
        called_script='.'.join(package_rel_path.split("/")[-1].split(".")[:-1]),
        option_list=option_list,
        tool_description=description,
    )
    data = dict(xdict="helllo")
    return render(request, 'sangerdev/index.html', data)



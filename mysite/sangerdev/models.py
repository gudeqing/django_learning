from django.db import models

# Create your models here.


class WebAPI(models.Model):
    api_name = models.CharField(max_length=100, default="xa_xb")
    package_rel_path = models.CharField(max_length=200, default="/*/*.py")
    description = models.CharField(max_length=500, default="simple description")

    def __str__(self):
        return self.api_name


class Arg(models.Model):
    api_name = models.ForeignKey(WebAPI, on_delete=models.CASCADE)
    arg_types = ['int', 'float', 'string', 'infile', 'outfile', ]
    arg_name = models.CharField(max_length=80)
    arg_type = models.CharField(
        max_length=20,
        choices=zip(arg_types, arg_types),
        default="string",
    )
    arg_default = models.CharField(max_length=100, default=None)
    arg_format = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.arg_name


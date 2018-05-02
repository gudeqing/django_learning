from django.db import models

# Create your models here.


class WebAPI(models.Model):
    api_name = models.CharField(max_length=100, help_text="Example: ref_rna.exp_venn")
    package_rel_path = models.CharField(max_length=200, help_text="Example: ref_rna.exp_venn_package")
    controller = models.CharField(max_length=100, help_text="Example: ref_rna_controller")

    def __str__(self):
        return self.api_name


class Arg(models.Model):
    api_name = models.ForeignKey(WebAPI, on_delete=models.CASCADE)
    arg_types = ['int', 'float', 'string', 'infile', 'outfile', ]
    arg_name = models.CharField(max_length=100, help_text="Argument Name")
    arg_type = models.CharField(
        max_length=20,
        choices=zip(arg_types, arg_types),
        default="string",
        help_text="Argument Type"
    )
    arg_default = models.CharField(max_length=100, default='None', help_text="Default Value")
    arg_format = models.CharField(max_length=100, default='None', help_text="Format Example: ref_rna.exp_matrix")

    def __str__(self):
        return self.arg_name


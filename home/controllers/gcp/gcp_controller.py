from ...models.tech_family import TechFamily
from django.shortcuts import render

def index(self, *args, **kwargs):
    tf = TechFamily.objects.order_by('name')
    context = {"ft_list": tf}
    return render( self, "gcp/index.html", context)

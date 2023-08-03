from ...models import TechFamily
from django.shortcuts import render

def index(self, *args, **kwargs):
    tf = TechFamily.objects.order_by('name')
    
    context = {"ft_list": tf}
    return render( self, "kubecost/index.html", context)
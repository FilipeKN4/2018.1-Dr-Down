from django.conf.urls import url
from django.views.generic import TemplateView


app_name = 'core'
urlpatterns = [
    url(
        regex=r'^$',
        view=TemplateView.as_view(template_name='core/home.html'),
        name='home'
    ),
    url(
        regex=r'^info/$',
        view=TemplateView.as_view(template_name='core/info.html'),
        name='about'
    ),
    url(
        regex=r'^vaccine/$',
        view=TemplateView.as_view(template_name='core/vaccine_schedule.html'),
        name='vaccine'
    ),
    url(
       regex=r'^vaccine/location$',
       view=TemplateView.as_view(template_name='core/vaccination_sites.html'),
       name='locations'
    ),

]

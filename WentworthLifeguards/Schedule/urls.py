from django.conf.urls import url
from . import views

urlpatterns = [
    #/Schedule/ <!-- The Landing Page
    url(r'^$', views.index, name='index'),
    #/Schedule/rota/ <!-- The Rota Display Page
    url(r'^rotas', views.rota, name='rota'),
    #Schedule/staffmanage or adminmanage/ <!-- The Shift Management Page
    url(r'^manage', views.manage, name = 'manage'),
    #/Schedule/loginsuccess/ <!-- The Login Success Notice Page
    url(r'^loginsuccess', views.loginsuccess, name='loginsuccess'),
    #/Schedule/provisionalrota <!-- The Provisional Rota Display Page
    url(r'^provisionalrota', views.provisionalrota, name = 'provisionalrota'),
]



from django.contrib import admin
from django.urls import path, re_path  
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index.as_view(), name='index'),
    path('registro/', registro.as_view(), name='registro'),
    path('pagar/', pagar.as_view(), name='pagar'),
    path('guardaPagos/', guardaPagos, name='guardaPagos'),
    path('consulta_deudas/', consulta_deudas.as_view(), name='consulta_deudas'),
    path('consulta_cobros/', consulta_cobros.as_view(), name='consulta_cobros'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^media(?P<path>.*)', serve, {
    'document_root': settings.MEDIA_ROOT,
    })
]



import datetime
from datetime import date
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from requests import post
from core.forms import CambiaContrasenaForm
from core.funciones import f_anio_mes_str, llena_mantenimiento 
from .models import *
from django.db.models.aggregates import Count
from django.db.models import Sum
from core.funciones import genera_cobros, llena_mantenimiento
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class index(ListView):
    model = Edificio
    template_name = 'core/index.html'
    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context["deptos"] = D_DEPTO
        context["servicios"] = Servicio.objects.all()
        return context

class registro(LoginRequiredMixin, ListView):
    template_name = 'core/registro.html'
    def get_context_data(self, **kwargs):
        context = super(registro, self).get_context_data(**kwargs)
        edificio = self.request.GET['edificio']
        depto = self.request.GET['depto']
        servicio = self.request.GET['servicio']
        servicios = Servicio.objects.all().filter(id=servicio).first()
        field_object = servicios._meta.get_field('descripcion')
        descripcion = field_object.value_from_object(servicios)
        context['nomServicio'] = descripcion
        context['edificio'] = edificio
        context['depto'] = depto
        context['servicio'] = servicio
        return context
    def get_queryset(self):
        edificio = self.request.GET['edificio']
        depto = self.request.GET['depto']
        servicio = self.request.GET['servicio']
        queryset = Matto.objects.filter(edificio=edificio, depto=depto, servicio=servicio).order_by('anio', 'mes')
        return queryset

class pagar(LoginRequiredMixin, ListView):
    template_name = 'core/pagar.html'
    def get_context_data(self, **kwargs):
        context = super(pagar, self).get_context_data(**kwargs)
        edificio = self.request.GET['edificio']
        depto = self.request.GET['depto']
        servicio = self.request.GET['servicio']
        Pagos = []
        numero_pagos = 0;
        for param in self.request.GET:
            if param.startswith('cb-'):
                anio = param[3:7]
                mes = param[8:10]
                Pagos.append({"anio": anio, "mes": mes})
                numero_pagos += 1
        servicios = Servicio.objects.all().filter(id=servicio).first()
        field_object = servicios._meta.get_field('descripcion')
        descripcion = field_object.value_from_object(servicios)
        field_object = servicios._meta.get_field('importe')
        importe = field_object.value_from_object(servicios)
        total = numero_pagos * importe
        context['edificio'] = edificio
        context['depto'] = depto
        context['servicio'] = servicio
        context['nomServicio'] = descripcion
        context['importe'] = importe
        context['Pagos'] = Pagos
        context['total'] = total
        context['totalPagos'] = numero_pagos
        return context
    def get_queryset(self):
        edificio = self.request.GET['edificio']
        depto = self.request.GET['depto']
        servicio = self.request.GET['servicio']
        queryset = Matto.objects.filter(edificio=edificio, depto=depto, servicio=servicio).order_by('anio', 'mes')
        return queryset

@login_required
def guardaPagos(self):
    edificio = self.GET['edificio']
    depto = self.GET['depto']
    servicio = self.GET['servicio']
    recibo = self.GET['recibo']
    pagos = self.GET['pagos']
    recibimosDe = self.GET['recibimosDe']
    importe = self.GET['importe']
    nomServicio = self.GET['nomServicio']
    usuarioId = self.user.id
    nom_usuario = self.user.username
    with transaction.atomic():
        reciboFisico = Recibo(numero_recibo=recibo , edificio=edificio , depto=depto , nom_usuario=nom_usuario, \
            recibimos_de=recibimosDe , importe=importe , concepto= nomServicio, usuario_id=usuarioId )
        reciboFisico.save()
        numero_recibo = reciboFisico.id
        vuelta = 'anio'
        indice = 0
        ini = 0
        fin = 0
        for p in pagos:
            if p == ':':
                if vuelta == 'anio':
                    ini = indice + 3
                    fin = indice + 7
                    anio = pagos[ini:fin]
                    vuelta = 'mes'
                else:
                    ini = indice + 3
                    fin = indice + 5
                    mes = pagos[ini:fin]
                    vuelta = 'anio'
                    characters = "'"
                    mes = ''.join( x for x in mes if x not in characters)
                    pago_act = Matto.objects.filter(edificio=edificio,depto=depto, servicio=servicio, anio=anio, mes=mes). \
                        update(recibo=recibo, reciboFisico=numero_recibo, estatus=1, usuario_id=usuarioId)
            indice += 1
    return redirect('index')

class consulta_deudas(LoginRequiredMixin, ListView):
    template_name = 'core/consulta_adeudos.html'
    def get_context_data(self, **kwargs):
        context = super(consulta_deudas, self).get_context_data(**kwargs)
        servicios = Servicio.objects.all()
        context['servicios'] = servicios
        context["deptos"] = D_DEPTO
        context["edificios"] = Edificio.objects.all()
        edificio = self.request.GET.get('edificio')
        depto = self.request.GET.get('depto')
        servicio = self.request.GET.get('servicio')
        if edificio == None:
            edificio = '00'
        if depto == None:
            depto = '000'
        if servicio == None:
            servicio = '0'
        context['edificio'] = edificio
        context["depto"] = depto
        context["servicio"] = servicio
        return context
    def get_queryset(self):
        anio_act = datetime.datetime.today().year
        mes_act = datetime.datetime.today().month
        if mes_act == 1:
            year -= 1
            mes_act = 12
        else:
            mes_act -= 1
        anio = str(anio_act)
        mes = str(mes_act)
        if mes_act < 10:
            mes = "0" + mes
        hasta = anio + mes
        edificio = self.request.GET.get('edificio','0')
        depto = self.request.GET.get('depto','0')
        servicio = self.request.GET.get('servicio','0')
        queryset = Matto.objects.values('edificio','depto','servicio') \
            .annotate(dcount=Count('edificio')).order_by('edificio','depto','servicio_id') \
            .filter(estatus=0,hasta__lt=hasta)
        if edificio == None:
            edificio = '00'
        if depto == None:
            depto = '000'
        if servicio == None:
            servicio = '0'
        if edificio > "00":
            queryset = queryset.filter(edificio=edificio)
        if depto > "000":
            queryset = queryset.filter(depto=depto)
        if servicio > "0":
            queryset = queryset.filter(servicio_id=servicio)
        return queryset
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return self.reverse_lazy(self.get_context_data(form=form))

class consulta_cobros(LoginRequiredMixin, ListView):
    template_name = 'core/consulta_cobros.html'
    def get_context_data(self, **kwargs):
        context = super(consulta_cobros, self).get_context_data(**kwargs)
        servicios = Servicio.objects.all()
        context['servicios'] = servicios
        context["deptos"] = D_DEPTO
        context["edificios"] = Edificio.objects.all()
        edificio = self.request.GET.get('edificio')
        depto = self.request.GET.get('depto')
        servicio = self.request.GET.get('servicio')
        if edificio == None:
            edificio = '00'
        if depto == None:
            depto = '000'
        if servicio == None:
            servicio = 'Todos'
        context['edificio'] = edificio
        context["depto"] = depto
        context["servicio"] = servicio
        buscar = self.request.GET.get('buscar')
        context["buscar"] = buscar
        if buscar == 'lugar':
            anio_str = str(datetime.datetime.today().year)
            mes = datetime.datetime.today().month
            dia = datetime.datetime.today().day
            if dia < 10:
                dia_str = '0' + str(dia)
            else:
                dia_str = str(dia)
            if mes < 10:
                mes_str = '0' + str(mes)
            else:
                mes_str = str(mes)
            Hoy = anio_str + '-' + mes_str + '-' + dia_str
            fechaDesde = Hoy
            FechaHasta = Hoy
            context["fechaDesde"] = fechaDesde
            context["FechaHasta"] = FechaHasta
        else:
            fechaDesde = self.request.GET.get('fechaDesde')
            FechaHasta = self.request.GET.get('fechaHasta')
            context["fechaDesde"] = fechaDesde
            context["FechaHasta"] = FechaHasta
        return context
    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        if buscar == 'lugar':
            edificio = self.request.GET.get('edificio','0')
            depto = self.request.GET.get('depto','0')
            servicio = self.request.GET.get('servicio')
            queryset = Recibo.objects \
                .values('edificio', 'depto', 'concepto', 'nom_usuario') \
                .annotate(dcount=Count('edificio'),dimporte=Sum('importe')) \
                .order_by('edificio', 'depto', 'concepto', 'nom_usuario')
            if edificio == None:
                edificio = '00'
            if depto == None:
                depto = '000'
            if servicio == None:
                servicio = 'Todos'
            if edificio > "00":
                queryset = queryset.filter(edificio=edificio)
            if depto > "000":
                queryset = queryset.filter(depto=depto)
            if servicio != "Todos":
                queryset = queryset.filter(concepto=servicio)
        else:
            fechaDesde = self.request.GET.get('fechaDesde')
            FechaHasta = self.request.GET.get('fechaHasta')
            Hoy = date.today()
            if fechaDesde == "":
                fechaDesde = Hoy
            if FechaHasta == "":
                FechaHasta = Hoy
            queryset = Recibo.objects \
                .filter(fecha_pago__range=[fechaDesde, FechaHasta]) \
                .values('edificio', 'depto', 'concepto', 'nom_usuario') \
                .annotate(dcount=Count('edificio'),dimporte=Sum('importe')) \
                .order_by('edificio', 'depto', 'concepto', 'nom_usuario') 
        return queryset
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return self.reverse_lazy(self.get_context_data(form=form))

class genera_recibos(LoginRequiredMixin, ListView):
    template_name = 'core/genera_recibos.html'
    def get_context_data(self, **kwargs):
        context = super(genera_recibos, self).get_context_data(**kwargs)
        servicios = Servicio.objects.all()
        context["servicios"] = servicios
        context["anio"] = ANIO
        context["mes"] = MES_O
        return context
    def get_queryset(self):
        queryset = Matto.objects.all()
        return queryset
    def post(self, request, *args, **kwargs):
#        llena_mantenimiento(self, request)
        servicio = int(request.POST.get('servicio'))
        anio = int(request.POST.get('anio'))
        mes = int(request.POST.get('mes'))
        genera_cobros(anio, mes, servicio)
        return redirect('genera_recibos')

class cambiar_contrasena(LoginRequiredMixin, View):
    template_name = 'core/cambiar_contrasena.html'
    form_class = CambiaContrasenaForm
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs ):
        return render(request, self.template_name, {'form': self.form_class})
    
    def post(self, request, *args, **kwargs ):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = Usuario.objects.filter(id=request.user.id)
            if user.exists(): 
                user = user.first()
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form': form})

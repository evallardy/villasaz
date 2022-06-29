import datetime
from msilib.schema import ListView
from unittest import result

from .models import *
import numpy as np

def f_anio_mes_str():
    anio = datetime.datetime.today().year
    mes = datetime.datetime.today().month
    if mes < 10:
        mes_str = "0" + str(mes)
    else:
        mes_str = str(mes)
    resultado = str(anio) + mes_str 
    return resultado

def genera_cobros(anio, mes_num, servicio):
    consulta0 = Matto.objects.filter(servicio=servicio, anio=anio, mes=mes_num)
    registros = consulta0.count()
    if mes_num < 10:
        mes_str = "0" + str(mes_num)
    else:
        mes_str = str(mes_num)
    hasta = str(anio) + mes_str
    if registros == 0:
        edificio = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27']
        depto = ['001','002','003','004','101','102','103','104','201','202','203','204','301','302','303','304','401','402','403','404']
        for  e in edificio:
            for d in depto:
                mantto = Matto(edificio=e, depto=d, servicio_id=servicio, anio=anio, mes=mes_num, hasta=hasta)
                mantto.save()

def llena_mantenimiento():
    anio = datetime.datetime.today().year
    mes = datetime.datetime.today().month
    servicios = Servicio.objects.all()
    anio_hasta = anio + 2
    for s in servicios:
        id_servicio = s.id
        consulta0 = Matto.objects.filter(servicio=id_servicio, anio=anio_hasta, mes=mes)
        registros = consulta0.count()
        if registros == 0:
            anios = np.arange(anio,anio_hasta,1,int) 
            meses = np.arange(1,13,1,int) 
            for  a in anios:
                for m in meses:
                    consulta1 = Matto.objects.filter(servicio=id_servicio, anio=a, mes=m)
                    registros = consulta1.count()
                    if registros == 0:
                        genera_cobros(a, m, id_servicio)

def cambia_ddmmaaaa_aaaammdd(campo):
    dia = campo[0:2]
    mes = campo[3:5]
    anio = campo[6:]
    return anio + "-" - mes + "-" + dia

def cambia_aaaammdd_ddmmaaaa(campo):
    dia = campo[8:]
    mes = campo[5:7]
    anio = campo[0:4]
    return dia + "-" - mes + "-" + anio
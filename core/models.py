from django.db import models
from django.contrib.auth.models import AbstractUser


ESTATUS_PAGO = (
    ('0', 'Pendiente'),
    ('1', 'Pagado'),
)
RESPONSABLE = (
    ('1', 'Administrador'),
    ('2', 'Tesorero'),
    ('3', 'Inquilino'),
)
ANIO = {
    (2018),
    (2019),
    (2020),
    (2021),
    (2022),
    (2023),
    (2024),
}
MES = (
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre'),
)
MES_O = (
    {'mes':1, 'nombre':'Enero'},
    {'mes':2, 'nombre':'Febrero'},
    {'mes':3, 'nombre':'Marzo'},
    {'mes':4, 'nombre':'Abril'},
    {'mes':5, 'nombre':'Mayo'},
    {'mes':6, 'nombre':'Junio'},
    {'mes':7, 'nombre':'Julio'},
    {'mes':8, 'nombre':'Agosto'},
    {'mes':9, 'nombre':'Septiembre'},
    {'mes':10, 'nombre':'Octubre'},
    {'mes':11, 'nombre':'Noviembre'},
    {'mes':12, 'nombre':'Diciembre'},
)
EDIFICIO = (
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('04', '04'),
    ('05', '05'),
    ('06', '06'),
    ('07', '07'),
    ('08', '08'),
    ('09', '09'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('24', '24'),
    ('25', '25'),
    ('26', '26'),
    ('27', '27'),
)
DEPTO = (
    ('001', '001'),
    ('002', '002'),
    ('003', '003'),
    ('004', '004'),
    ('101', '101'),
    ('102', '102'),
    ('103', '103'),
    ('104', '104'),
    ('201', '201'),
    ('202', '202'),
    ('203', '203'),
    ('204', '204'),
    ('301', '301'),
    ('302', '302'),
    ('303', '303'),
    ('304', '304'),
    ('401', '401'),
    ('402', '402'),
    ('403', '403'),
    ('404', '404'),
)
D_DEPTO = (
    ('001'),
    ('002'),
    ('003'),
    ('004'),
    ('101'),
    ('102'),
    ('103'),
    ('104'),
    ('201'),
    ('202'),
    ('203'),
    ('204'),
    ('301'),
    ('302'),
    ('303'),
    ('304'),
    ('401'),
    ('402'),
    ('403'),
    ('404'),
)
class Edificio(models.Model):
    numero = models.CharField("Edificio", max_length=2)
    coordenadas = models.CharField("Coordenadas", max_length=255)
    etiqueta_x = models.CharField("Etiqueta X", max_length=5)
    etiqueta_y = models.CharField("Etiqueta Y", max_length=5)

    class Meta:
        verbose_name = 'Edificio'
        verbose_name_plural = 'Edificios'
        ordering = ['numero']
        unique_together= (('numero',),)
        db_table = 'Edificio'

    def __str__(self):
        return 'Edificio %s' % (self.numero)

class Usuario(AbstractUser):  
    materno = models.CharField("Nombre", max_length=30, blank=True, null=True)
    celular = models.CharField("Celular", max_length=30, blank=True, null=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['first_name', 'last_name', 'materno']
        db_table = 'Usuario'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def _get_nombre_completo(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.materno)
    nombre_completo = property(_get_nombre_completo)

class Recibo(models.Model):
    numero_recibo = models.CharField("Número de recibo", max_length=30)
    edificio = models.CharField("Edificio", max_length=2, choices=EDIFICIO)
    depto = models.CharField("Departamento", max_length=3, choices=DEPTO)
    recibimos_de = models.CharField("Departamento", max_length=90)
    importe = models.DecimalField("Importe", max_digits=9, decimal_places=2, default=0)
    concepto = models.CharField("Concepto", max_length=500)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pago = models.DateField("FecahPago", auto_now_add=True, blank=True, null=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'
        ordering = ['edificio','depto','-created']
        db_table = 'Recibo'

    def __str__(self):
        return '%s-%s %s %s $ %s' % (self.edificio, self.depto, self.fecha_pago, self.concepto, self.importe)

class Servicio(models.Model):
    descripcion = models.CharField("Servicio", max_length=100)
    importe = models.DecimalField("importe", max_digits=9, decimal_places=2, default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['descripcion']
        unique_together= (('descripcion',),)
        db_table = 'Servicio'

    def __str__(self):   # para poner los nombre en los renglones
        return '%s $ %s' % (self.descripcion, self.importe)

class Matto(models.Model):
    edificio = models.CharField("Edificio", max_length=2, choices=EDIFICIO)
    depto = models.CharField("Departamento", max_length=3, choices=DEPTO)
    servicio = models.ForeignKey("Servicio", on_delete=models.CASCADE, verbose_name="servicio_matto")
    anio = models.IntegerField("Año")
    mes = models.IntegerField("Mes", choices=MES)
    hasta = models.CharField("Año - mes", max_length=6, default='000000') 
    recibo = models.CharField("Número de recibo", max_length=30, blank=True, null=True)
    reciboFisico = models.ForeignKey(Recibo, on_delete=models.CASCADE, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    estatus = models.IntegerField("Estatus servicio", choices=ESTATUS_PAGO, default=0)

    class Meta:
        verbose_name = 'Matto'
        verbose_name_plural = 'Mattos'
        ordering = ['edificio','depto', 'servicio', '-anio', '-mes']
        unique_together= (('edificio','depto', 'servicio', 'anio', 'mes'),)
        db_table = 'Matto'

    def __str__(self):
        return '%s-%s %s %s/%s ' % (self.edificio, self.depto, self.servicio, self.anio, self.mes)

    def _get_anio_mes(self):
        if self.mes < 10:
            mes = "0" + str(self.mes)
        else:
            mes = str(self.mes)
        anio = str(self.anio)
        return anio + mes
    anio_mes = property(_get_anio_mes)

class Contacto(models.Model):
    edificio = models.CharField("Edificio", max_length=2, choices=EDIFICIO)
    depto = models.CharField("Departamento", max_length=3, choices=DEPTO)
    nombre = models.CharField("Nombre", max_length=90)
    celular = models.CharField("Celular", max_length=60, blank=True, null=True)
    telefono = models.CharField("Teléfono", max_length=60, blank=True, null=True)
    correo = models.EmailField("Correo", blank=True, null=True)
    responsable = models.IntegerField("Responsabilidad", choices=RESPONSABLE)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['edificio', 'depto']
        unique_together= (('edificio', 'depto', 'nombre'),)
        db_table = 'Contacto'

    def __str__(self):   # para poner los nombre en los renglones
        return '%s-%s  %s' % (self.edificio, self.depto, self.nombre)

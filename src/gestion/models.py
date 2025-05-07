from django.db import models

# Create your models here.
class Medico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    horario_disponible = models.TextField()  # Ej: JSON con días y horas
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

class Cita(models.Model):
    id = models.AutoField(primary_key=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=15, choices=[('programada', 'Programada'), ('completada', 'Completada'), ('cancelada', 'Cancelada')])

class HistoriaMedica(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historial')
    fecha = models.DateField()
    descripcion = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()

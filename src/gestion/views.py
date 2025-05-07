from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Medico, Paciente, Cita, HistoriaMedica
from .serializers import MedicoSerializer, PacienteSerializer, CitaSerializer, HistoriaMedicaSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer

    @action(detail=True, methods=['get'])
    def disponibilidad(self, request, pk=None):
        medico = self.get_object()
        fecha = request.query_params.get('fecha')
        if not fecha:
            return Response({"error": "Parámetro 'fecha' requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filtrar citas del médico para la fecha
        citas = Cita.objects.filter(medico=medico, fecha_hora__date=fecha)
        horas_ocupadas = [cita.fecha_hora.strftime("%H:%M") for cita in citas]
        
        # Aquí deberías calcular horas libres según el horario del médico (simplificado)
        disponibilidad_ejemplo = ["08:00", "09:00", "10:00", "11:00", "12:00"]
        horas_disponibles = [h for h in disponibilidad_ejemplo if h not in horas_ocupadas]

        return Response({"fecha": fecha, "horas_disponibles": horas_disponibles})

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    @action(detail=True, methods=['get'])
    def historial(self, request, pk=None):
        paciente = self.get_object()
        historial = HistoriaMedica.objects.filter(paciente=paciente)
        serializer = HistoriaMedicaSerializer(historial, many=True)
        return Response(serializer.data)

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer

    @action(detail=True, methods=['put'])
    def reprogramar(self, request, pk=None):
        cita = self.get_object()
        nueva_fecha = request.data.get('nueva_fecha_hora')
        if not nueva_fecha:
            return Response({'error': 'Se requiere nueva_fecha_hora'}, status=status.HTTP_400_BAD_REQUEST)
        
        cita.fecha_hora = nueva_fecha
        cita.save()
        return Response(self.get_serializer(cita).data)

    @action(detail=True, methods=['put'])
    def cancelar(self, request, pk=None):
        cita = self.get_object()
        cita.estado = 'cancelada'
        cita.save()
        return Response({'mensaje': 'Cita cancelada correctamente'})

class HistoriaMedicaViewSet(viewsets.ModelViewSet):
    queryset = HistoriaMedica.objects.all()
    serializer_class = HistoriaMedicaSerializer

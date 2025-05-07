from rest_framework import serializers
from .models import Medico, Paciente, Cita, HistoriaMedica

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class CitaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(read_only=True)
    paciente = PacienteSerializer(read_only=True)
    medico_id = serializers.PrimaryKeyRelatedField(queryset=Medico.objects.all(), source='medico', write_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), source='paciente', write_only=True)

    class Meta:
        model = Cita
        fields = ['id', 'fecha_hora', 'motivo', 'estado', 'medico', 'paciente', 'medico_id', 'paciente_id']

class HistoriaMedicaSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), source='paciente', write_only=True)

    class Meta:
        model = HistoriaMedica
        fields = ['id', 'fecha', 'descripcion', 'diagnostico', 'tratamiento', 'paciente', 'paciente_id']

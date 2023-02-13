from rest_framework import serializers
from myapp.models import Barrio


class BarrioSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)

    class Meta:
        model = Barrio

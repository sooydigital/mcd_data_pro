from rest_framework import serializers
from myapp.models import Barrio


class BarrioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Barrio
        # fields = ['id', 'name']
from rest_framework import serializers
from lcperformance.models import comite, weekly, product, od_stage


class ComiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = comite
        fields = ('id', 'name', 'code_od_stage', 'code_expa', 'code_podio')

    def create(self, validated_data):
        return comite.objects.create(**validated_data)

class WeeklySerializer(serializers.ModelSerializer):
    class Meta:
        model = weekly
        fields = ('id', 'init_date', 'final_date', 'name')

    def create(self, validated_data):
        return weekly.objects.create(**validated_data)

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ('id', 'name', 'type_expa', 'code_expa')

    def create(self, validated_data):
        return product.objects.create(**validated_data)

class OdStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = od_stage
        fields = ('id', 'name')

    def create(self, validated_data):
        return od_stage.objects.create(**validated_data)

class LCPerformance(serializers.Serializer):
    id = serializers.IntegerField()

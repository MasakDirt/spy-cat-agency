from django.db import transaction
from rest_framework import serializers

from spy_agency.models import SpyCat, Target, Mission


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ("id", "name", "years_of_experience", "breed", "salary")


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "name", "country", "notes", "is_complete", "mission")
        read_only_fields = ("id", "mission")


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ("id", "is_complete", "cat", "targets")

    def create(self, validated_data: dict) -> Mission:
        targets_data = validated_data.pop("targets")
        with transaction.atomic():
            mission = Mission.objects.create(**validated_data)
            for target_data in targets_data:
                Target.objects.create(mission=mission, **target_data)

        return mission

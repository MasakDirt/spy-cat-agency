from django.db import transaction
from rest_framework import serializers

from spy_agency.models import SpyCat, Target, Mission


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ("id", "name", "years_of_experience", "breed", "salary")

    def update(self, instance, validated_data):
        if "salary" in validated_data:
            instance.salary = validated_data["salary"]
            instance.save()
        return instance


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "name", "country", "notes", "is_complete", "mission")
        read_only_fields = ("id", "mission")


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "notes", "is_complete")
        read_only_fields = ('id',)


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


class MissionListSerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source="cat.name")
    cat_breed = serializers.CharField(source="cat.breed")
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ("id", "is_complete", "cat_name", "cat_breed", "targets")


class MissionDetailSerializer(MissionSerializer):
    cat = SpyCatSerializer()

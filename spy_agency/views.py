from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from spy_agency.models import SpyCat, Mission, Target
from spy_agency.serializers import (
    SpyCatSerializer,
    MissionSerializer,
    TargetSerializer, MissionListSerializer, MissionDetailSerializer,
)


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def get_queryset(self) -> QuerySet[Mission]:
        queryset = super().get_queryset()

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related(
                "cat"
            ).prefetch_related("targets")

        return queryset

    def get_serializer_class(self) -> ModelSerializer:
        serializer = super().get_serializer_class()

        if self.action == "list":
            serializer = MissionListSerializer
        if self.action == "retrieve":
            serializer = MissionDetailSerializer

        return serializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cat is not None:
            return Response(
                {"detail": "Cannot delete a mission assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def complete_target(self, request, pk=None):
        mission = self.get_object()
        target_id = request.data.get("target_id")

        target = get_object_or_404(Target, id=target_id)
        if mission.complete or target.complete:
            return Response(
                {"detail": "Cannot modify completed mission or target."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        target.complete = True
        target.save()

        serializer = TargetSerializer(target)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

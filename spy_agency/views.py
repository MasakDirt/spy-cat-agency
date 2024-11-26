from django.db import transaction
from django.db.models import QuerySet
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from spy_agency.models import SpyCat, Mission, Target
from spy_agency.serializers import (
    SpyCatSerializer,
    MissionSerializer,
    TargetSerializer, MissionListSerializer, MissionDetailSerializer,
    TargetUpdateSerializer,
)


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
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
        if self.action == "update_targets":
            serializer = TargetUpdateSerializer

        return serializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cat is not None:
            return Response(
                {"detail": "Cannot delete a mission assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["patch"])
    def update_targets(self, request, pk=None):
        mission = self.get_object()
        targets_data = request.data.get("targets", [])

        if not targets_data:
            return Response(
                {"detail": "No targets data provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated_targets = []
        with transaction.atomic():
            for target_data in targets_data:
                target_id = target_data.get("id")
                if not target_id:
                    return Response(
                        {"detail": "Target ID is required for each target."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                target = get_object_or_404(Target, id=target_id)
                if target.mission_id != mission.id:
                    return Response(
                        {
                            "detail": f"Target ID {target_id} "
                                      f"is not part of this mission."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if mission.is_complete or target.is_complete:
                    return Response(
                        {
                            "detail": f"Cannot modify completed target "
                                      f"(ID {target_id}) or mission."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                serializer = TargetUpdateSerializer(
                    target,
                    data=target_data,
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_targets.append(serializer.data)

        return Response(
            updated_targets,
            status=status.HTTP_200_OK
        )

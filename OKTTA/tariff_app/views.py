from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, mixins
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta

from common.permissions import IsUserNotManager
from .models import Plan
from .serializers import UsersSerializer, PlanSerializer

User = get_user_model()

@extend_schema(
    tags=['plans'],
    summary='Получение списка тарифных планов',
    responses={200: PlanSerializer(many=True)},
)
class PlansViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated | IsUserNotManager]

@extend_schema(
    tags=['plans'],
    summary='приобретение тарифного плана',
    responses={200: PlanSerializer(many=True)},
)
class PlansUsersViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated | IsUserNotManager]

    @action(detail=True, methods=['patch'], url_path='purchase-plan')
    def purchase_plan(self, request, pk=None):
        user = self.get_object()
        plan_id = request.data.get('plan')

        if not plan_id:
            return Response({"error": "Необходимо указать ID тарифного плана."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"error": "Тарифный план не найден."}, status=status.HTTP_404_NOT_FOUND)

        tokens = plan.tokens
        user.tokens_purchased += tokens
        user.plan = plan
        user.plan_start_date = timezone.now()
        user.plan_end_date = timezone.now() + timedelta(days=30)
        user.save()

        return Response({"message": "Тарифный план успешно приобретен.", "plan": plan.name}, status=status.HTTP_200_OK)

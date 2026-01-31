from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from api_with_restrictions.advertisements.filters import AdvertisementFilter
from api_with_restrictions.advertisements.models import Advertisement
from api_with_restrictions.advertisements.permissions import IsAuthenticatedOrReadOnly
from api_with_restrictions.advertisements.serializers import AdvertisementSerializer, UserSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    serializer_user = UserSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticatedOrReadOnly()]
        return []

    def list(self, request):
        list = Advertisement.objects.all()
        queryset = AdvertisementFilter(data=request.GET, queryset=list, request=request).qs
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)

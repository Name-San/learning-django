from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin

class CustomCartModelViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    pass

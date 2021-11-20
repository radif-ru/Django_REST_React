from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from djangorestframework_camel_case.render import CamelCaseJSONRenderer, \
    CamelCaseBrowsableAPIRenderer

from .filters import TodoFilter
from .models import Todo
from .paginators import TodoLimitOffsetPagination
from .permissions import TodoPermission
from .serializers import TodoModelSerializer


class TodoModelViewSet(ModelViewSet):
    """Набор представлений для модели заметок"""
    permission_classes = [TodoPermission]
    renderer_classes = (
        # Верблюжий стиль JSON и браузерного API
        CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer
    )
    # Вывод только активных заметок
    queryset = Todo.objects.filter(active=1)
    serializer_class = TodoModelSerializer
    # Подключение кастомного пагинатора
    pagination_class = TodoLimitOffsetPagination

    # Подключение кастомного фильтра django-filter
    filterset_class = TodoFilter

    def destroy(self, request, *args, **kwargs):
        """ Переопределения метода удаления (DELETE)
        Вместо фактического удаления меняем активность на 0 (False)
        """
        instance = self.get_object()
        instance.active = 0
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
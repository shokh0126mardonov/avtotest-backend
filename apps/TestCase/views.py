import random

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.permissions import AdminPermissions
from .models import TestAnswer,TestCase
from .serializers import TestCaseSerializers,TestCaseCreateSerializers
from .spectacular import list_schema,retrieve_schema
from .pagination import TestCasePagination


class TestCaseViewSets(ModelViewSet):
    permission_classes = [IsAuthenticated,AdminPermissions]
    authentication_classes = [JWTAuthentication]
    queryset = TestCase.objects.all()
    pagination_class = TestCasePagination

    def get_serializer_class(self):
        if self.action in ['create','partial_update']:
            return TestCaseCreateSerializers
        return TestCaseSerializers


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'uz')
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        lang = self.request.query_params.get('lang')
        if lang == 'uz':
            qs = qs.exclude(question_uz__isnull=True)
        elif lang == 'ru':
            qs = qs.exclude(question_ru__isnull=True)

        return qs
    
    @list_schema
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()

        is_random = request.query_params.get('random')
        
        if is_random == 'true':
            page_size = request.query_params.get('page_size')

            
            if not page_size:
                page_size = self.paginator.page_size
            else:
                page_size = int(page_size)

            ids = list(qs.values_list('id', flat=True))

            if not ids:
                return Response([])

            selected_ids = random.sample(ids, min(page_size, len(ids)))

            preserved = {id: index for index, id in enumerate(selected_ids)}
            random_qs = list(qs.filter(id__in=selected_ids))

            random_qs.sort(key=lambda x: preserved[x.id])

            serializer = self.get_serializer(random_qs, many=True)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)
    
    @retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
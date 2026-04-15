from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

list_schema = extend_schema(
    parameters=[
        OpenApiParameter(name='lang', type=OpenApiTypes.STR),
        OpenApiParameter(name='random', type=OpenApiTypes.BOOL),
        OpenApiParameter(name='page', type=OpenApiTypes.INT),
        OpenApiParameter(name='page_size', type=OpenApiTypes.INT),
    ]
)
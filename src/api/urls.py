from django.urls import path, re_path
from drf_yasg2 import openapi
from drf_yasg2.inspectors import view
from drf_yasg2.views import get_schema_view
from rest_framework.routers import SimpleRouter

from api.views import main_api_view, ArticlesViewSet

router = SimpleRouter()
router.register(r'articles', ArticlesViewSet, basename='article')
schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

app_name = 'api'
urlpatterns = [
    path('', main_api_view, name='main'),
    *router.urls,
    # path('articles/', view.SimpleRouterDetailView.as_view(), name='articles'),
    re_path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

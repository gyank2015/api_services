from django.contrib import admin
from django.urls import path, include
# from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings


schema_view = get_swagger_view(title='RESULT API')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view),
    path('result/', include('result_api_app.urls'), name='infer')
    # path('auth_api/', include('rest_framework.urls')),  # For the browsable api, using swagger now
]

from django.contrib import admin
from django.urls import path, include
# from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings


schema_view = get_swagger_view(title='CAR DAMAGE API')
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('')
    path('swagger/', schema_view),
    path('', include('car_damage_app.urls'), name='infer'),
    path('infer/', include('django.contrib.auth.urls')),
    # path('auth_api/', include('rest_framework.urls')),  # For the browsable api, using swagger now
]

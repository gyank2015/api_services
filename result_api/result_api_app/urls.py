from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    # path('<str:txnID>/<str:hash>', views.image_result.as_view(), name='image_result'),
    path('list/<str:txnID>',views.batch_result.as_view(), name='batch_result'),
    path('<str:txnID>',views.resultUI, name = 'resultUI'),
    path('list/<str:txnID>/<str:imagehashcluster>',views.imagehash_cluster_result.as_view(), name = 'imagehash_cluster_result')

]

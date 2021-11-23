from django.urls import path, include
from rest_framework import routers
from . import views
from . import api

router = routers.DefaultRouter()
router.register(r'transactions', api.TransactionViewSet)
router.register(r'transaction-importer', api.TransactionImporterViewSet, basename='transaction-importer')
router.register(r'spot-price', api.SpotPriceViewSet, basename='spot-price')

urlpatterns = [
    path('', views.index, name='index'),
    path('transactions', views.transactions, name='transactions'),
    path('transaction-importer', views.transaction_importer, name='transaction-importer'),
    path('api/', include(router.urls)),
]


urlpatterns += router.urls
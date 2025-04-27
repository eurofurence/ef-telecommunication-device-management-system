"""
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from backend.views.provision import ProvisionMetadataView, ProvisionConfigView, ProvisionPhonebookView, \
    ProvisionWallpaperView

"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend.views import UserViewSet, ItemOwnerViewSet, CurrentUserProfileView
from backend.views.binding import ItemBindingViewSet
from backend.views.callbox import CallboxTemplateViewSet, CallboxViewSet
from backend.views.item import QuickAddItemTemplatesViewSet, ItemCoordinatesViewSet, ItemMetadataViewSet
from backend.views.order import OrderViewSet
from backend.views.phone import PhoneTemplateViewSet, PhoneViewSet
from backend.views.radio import RadioDeviceViewSet, RadioDeviceTemplateViewSet, RadioAccessoryViewSet, \
    RadioAccessoryTemplateViewSet, PagerTemplateViewSet, PagerViewSet, RadioCodingViewSet
from backend.views.statistics import StatisticsView
from backend.views.eventlog import EventLogEntryViewSet

router = routers.DefaultRouter()
router.register(r'callbox_templates', CallboxTemplateViewSet)
router.register(r'callboxes', CallboxViewSet)
router.register(r'eventlog', EventLogEntryViewSet, basename='eventlog')
router.register(r'item_bindings', ItemBindingViewSet, basename='item_bindings')
router.register(r'item_coordinates', ItemCoordinatesViewSet)
router.register(r'item_metadata', ItemMetadataViewSet)
router.register(r'item_owners', ItemOwnerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'pager_templates', PagerTemplateViewSet)
router.register(r'pagers', PagerViewSet)
router.register(r'phone_templates', PhoneTemplateViewSet)
router.register(r'phones', PhoneViewSet)
router.register(r'quickadd_templates', QuickAddItemTemplatesViewSet, basename='quickadd_templates')
router.register(r'radio_accessories', RadioAccessoryViewSet)
router.register(r'radio_accessory_templates', RadioAccessoryTemplateViewSet, basename='radio_accessory_templates')
router.register(r'radio_codings', RadioCodingViewSet)
router.register(r'radio_templates', RadioDeviceTemplateViewSet)
router.register(r'radios', RadioDeviceViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    # API
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/statistics/', StatisticsView.as_view(), name='item_binding_statistics'),
    path('api/current_user/', CurrentUserProfileView.as_view(), name='current_user_profile'),

    path('api/provision/', ProvisionMetadataView.as_view(), name='provision_metadata'),
    path('api/provision/config/<str:mac>/', ProvisionConfigView.as_view(), name='provision_config'),
    path('api/provision/phonebook/<str:name>/', ProvisionPhonebookView.as_view(), name='provision_phonebook'),
    path('api/provision/wallpaper/', ProvisionWallpaperView.as_view(), name='provision_wallpaper'),

    # Admin UI
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        # Swagger UI
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

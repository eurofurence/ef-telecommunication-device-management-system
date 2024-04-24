from django.contrib import admin

from backend.models import *


admin.site.register(binding.ItemBinding)  # TODO
admin.site.register(eventlog.EventLogEntry)  # TODO
admin.site.register(order.Order)  # TODO


@admin.register(item.ItemOwner)
class ItemOwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'shortname']
    search_fields = ['name']
    ordering = ['name']


@admin.register(item.ItemTemplate, callbox.CallboxTemplate, phone.PhoneTemplate, radio.PagerTemplate, radio.RadioAccessoryTemplate)
class ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'owner']
    search_fields = ['name', 'description', 'owner']
    ordering = ['name', 'owner']


class ItemCoordinatesAdminInline(admin.StackedInline):
    model = item.ItemCoordinates
    extra = 0


@admin.register(item.Item, radio.Pager, radio.RadioAccessory)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_owner', 'serialnumber', 'notes', 'handed_out']
    search_fields = ['get_name', 'get_owner', 'serialnumber', 'notes']
    inlines = [ItemCoordinatesAdminInline]

    @admin.display(description="Name", ordering='template__name')
    def get_name(self, obj):
        return obj.template.name

    @admin.display(description="Owner", ordering='template__owner__name')
    def get_owner(self, obj):
        return obj.template.owner.name


@admin.register(callbox.Callbox)
class CallboxAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'notes', 'location', 'extension', 'network', 'has_camera']
    search_fields = ['get_name', 'notes', 'location', 'extension']
    inlines = [ItemCoordinatesAdminInline]

    @admin.display(description="Name", ordering='template__name')
    def get_name(self, obj):
        return obj.template.name


@admin.register(phone.Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'notes', 'location', 'extension', 'network', 'dhcp']
    search_fields = ['get_name', 'notes', 'location', 'extension']
    inlines = [ItemCoordinatesAdminInline]

    @admin.display(description="Name", ordering='template__name')
    def get_name(self, obj):
        return obj.template.name


@admin.register(radio.RadioCoding)
class RadioCodingAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'description']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(radio.RadioDevice)
class RadioDeviceAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_coding', 'get_owner', 'callsign', 'serialnumber', 'notes', 'handed_out']
    search_fields = ['get_name', 'get_coding', 'get_owner', 'callsign', 'serialnumber', 'notes']
    inlines = [ItemCoordinatesAdminInline]

    @admin.display(description="Name", ordering='template__name')
    def get_name(self, obj):
        return obj.template.name

    @admin.display(description="Owner", ordering='template__owner__name')
    def get_owner(self, obj):
        return obj.template.owner.name

    @admin.display(description="Coding", ordering='template__coding__name')
    def get_coding(self, obj):
        return obj.template.coding.name


@admin.register(radio.RadioDeviceTemplate)
class RadioDeviceTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_coding', 'description', 'owner']
    search_fields = ['name', 'get_coding', 'description', 'owner']
    ordering = ['name', 'coding__name', 'owner']

    @admin.display(description="Coding", ordering='coding__name')
    def get_coding(self, obj):
        return obj.coding.name


@admin.register(user.User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'ef_reg_id', 'ef_security_collar_id', 'last_seen', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'ef_reg_id', 'ef_security_collar_id']
    ordering = ['username']

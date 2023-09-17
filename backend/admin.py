from django.contrib import admin

from backend.models import *


admin.site.register(binding.ItemBinding)
admin.site.register(callbox.Callbox)
admin.site.register(callbox.CallboxTemplate)
admin.site.register(eventlog.EventLogEntry)
admin.site.register(item.Item)
admin.site.register(item.ItemTemplate)
admin.site.register(phone.Phone)
admin.site.register(phone.PhoneTemplate)
admin.site.register(radio.RadioAccessory)
admin.site.register(radio.RadioAccessoryTemplate)
admin.site.register(radio.RadioDevice)
admin.site.register(radio.RadioDeviceTemplate)
admin.site.register(user.User)
admin.site.register(user.ItemOwner)

from django.contrib import admin


from .models import (
        Organization,
        Membership,
        Event,
        Address,
        Venue,
        Registration,
        Entry,
        Owner,
        Guest,
        Team,
        DivisionInfo,
        DivisionTeam,
        DivisionEvent,
)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
admin.site.register(Organization, OrganizationAdmin)
# 
# 
# class MembershipAdmin(admin.ModelAdmin):
#     list_display = ('user', 'organization', 'role', 'selected')
#     search_fields = ('user__username', 'organization__name', 'role')
#     list_filter = ('role', 'selected')
# admin.site.register(Membership, MembershipAdmin)
# 
# 
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'event_type', 'start_date', 'end_date', 'status')
    search_fields = ('name', 'organization__name', 'event_type')
    list_filter = ('status', 'event_type', 'start_date', 'end_date')
    date_hierarchy = 'start_date'
admin.site.register(Event, EventAdmin)
# 
# 
# class AddressAdmin(admin.ModelAdmin):
#     list_display = ('user', 'name', 'street', 'city', 'state', 'postal_code')
#     search_fields = ('user__username', 'name', 'street', 'city', 'state', 'postal_code')
#     list_filter = ('created_at', 'updated_at')
# admin.site.register(Address, AddressAdmin)
# 
# 
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'event', 'status', 'created_at')
    search_fields = ('event__name', 'status')
    list_filter = ('status', 'created_at')
    date_hierarchy = 'created_at'
admin.site.register(Registration, RegistrationAdmin)
# 
# 
# class OwnerAdmin(admin.ModelAdmin):
#     list_display = ('guest', 'auth_user', 'contact', 'created_at')
#     search_fields = ('guest__uuid', 'user__username')
#     list_filter = ('created_at',)
# admin.site.register(Owner, OwnerAdmin)
# 
# 
# class GuestAdmin(admin.ModelAdmin):
#     list_display = ('uuid', 'first_name', 'last_name', 'email', 'phone', 'created_at')
#     search_fields = ('uuid', 'name', 'email', 'phone')
#     list_filter = ('created_at',)
# admin.site.register(Guest, GuestAdmin)
# 
# 

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__guest__uuid')
    list_filter = ('created_at',)
admin.site.register(Team, TeamAdmin)



class DivisionInfoAdmin(admin.ModelAdmin):
    list_display = ('gender', 'age', 'level', 'created_at')
    list_filter = ('created_at',)
admin.site.register(DivisionInfo, DivisionInfoAdmin)


class DivisionTeamAdmin(admin.ModelAdmin):
    list_display = ('team', 'info', 'created_at')
    list_filter = ('created_at',)
admin.site.register(DivisionTeam, DivisionTeamAdmin)


class EntryAdmin(admin.ModelAdmin):
    list_display = ('registration', 'reported_division', 'assigned_division', 'status', 'created_at')
    list_filter = ('status', 'created_at')
admin.site.register(Entry, EntryAdmin)

 

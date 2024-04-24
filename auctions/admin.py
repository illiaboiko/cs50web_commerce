from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(User)

class BidInline(admin.TabularInline):
    model = Bid
    extra = 0

class ListingAdmin(admin.ModelAdmin):
    inlines = [BidInline]

admin.site.register(Listing, ListingAdmin)

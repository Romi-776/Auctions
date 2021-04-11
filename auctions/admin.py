from django.contrib import admin

from .models import User, auction_listing, bid, comment

# Register your models here.

admin.site.register(User)
admin.site.register(auction_listing)
admin.site.register(bid)
admin.site.register(comment)

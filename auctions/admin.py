from django.contrib import admin
from .models import Category,Listing,User,Bids,Comments

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Comments)

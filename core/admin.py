from django.contrib import admin

# Register your models here.
from .models import Category, Transaction, TransactionImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name',)

class TransactionImageInline(admin.TabularInline):
    list_display = ('image_url', 'created_at', 'updated_at')
    model = TransactionImage
    extra = 1

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'category', 'amount', 'type', 'transaction_date')
    list_filter = ('category', 'type', 'user')
    search_fields = ('description', 'category__name')
    date_hierarchy = 'transaction_date'
    inlines = [TransactionImageInline]



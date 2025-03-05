from .models import VerificationLog
from django.contrib import admin

@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ('document', 'verified_at', 'is_valid', 'method', 'verified_by')
    list_filter = ('is_valid', 'method')
    search_fields = ('document__file_name', 'verified_by__username')
    readonly_fields = ('verified_at',)
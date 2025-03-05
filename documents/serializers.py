from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'file_name', 'digital_signature', 'uploaded_at']
        read_only_fields = ['digital_signature', 'uploaded_at']
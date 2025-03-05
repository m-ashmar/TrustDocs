from django.db import models
from users.models import User
import os
from django.urls import reverse

class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    file_name = models.CharField(max_length=255)
    digital_signature = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('download-file', args=[str(self.id)])
    
    def file_exists(self):
        return os.path.exists(self.file.path)
    @property
    def latest_verification(self):
        return self.verificationlog_set.order_by('-verified_at').first()
    
    def __str__(self):
        return f"{self.file_name} - {self.owner.national_id}"
    
class VerificationLog(models.Model):
    VERIFICATION_METHODS = [
        ('AUTO', 'تلقائي عند التنزيل'),
        ('MANUAL', 'يدوي عبر الواجهة'),
        ('API', 'طلب API'),
        ('CLI', 'أمر سطر الأوامر'),
    ]
    
    document = models.ForeignKey('Document', on_delete=models.CASCADE, verbose_name='المستند')
    verified_at = models.DateTimeField(auto_now_add=True, verbose_name='وقت التحقق')
    is_valid = models.BooleanField(verbose_name='صالح')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='تم التحقق بواسطة')
    method = models.CharField(max_length=10, choices=VERIFICATION_METHODS, default='AUTO', verbose_name='طريقة التحقق')
    error_details = models.TextField(blank=True, verbose_name='تفاصيل الخطأ')

    class Meta:
        verbose_name = 'سجل التحقق'
        verbose_name_plural = 'سجلات التحقق'
        ordering = ['-verified_at']

    def __str__(self):
        return f"{self.document} - {self.get_method_display()} - {'صالح' if self.is_valid else 'غير صالح'}"    
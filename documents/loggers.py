import logging

class MaskSensitiveDataFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'error_details'):
            # إخفاء البيانات الحساسة مثل المفاتيح
            record.error_details = record.error_details.replace(settings.SECRET_KEY, '*****')
        return True
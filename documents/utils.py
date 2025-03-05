from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from django.conf import settings
from cryptography.hazmat.primitives.asymmetric import padding
from .models import VerificationLog


def verify_document_signature(document):
    """
    تحقق من صحة التوقيع الرقمي للمستند
    """
    if not document.file:
        logger.error(f"Document {document.id} has no file attached")
        return False
        
    try:
        # تحميل الشهادة العامة
        with open(settings.SERVER_CERT_PATH, 'rb') as cert_file:
            cert = x509.load_pem_x509_certificate(cert_file.read())
        
        public_key = cert.public_key()
        
        # قراءة محتوى الملف
        with document.file.open('rb') as f:
            file_data = f.read()
        
        # التحقق من التوقيع
        public_key.verify(
            bytes.fromhex(document.digital_signature),
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        logger.info(f"Document {document.id} verified successfully")
        return True
        
    except Exception as e:
        logger.error(f"Verification failed for document {document.id}: {str(e)}")
        return False
    finally:
        # إعادة تعيين مؤشر الملف
        document.file.seek(0)

    
    
def log_verification(document, is_valid, user=None, method='AUTO', error_details=''):
    VerificationLog.objects.create(
        document=document,
        is_valid=is_valid,
        verified_by=user,
        method=method,
        error_details=error_details
    )
    
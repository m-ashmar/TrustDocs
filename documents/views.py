from django.shortcuts import render, redirect
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Document
from .serializers import DocumentSerializer
from users.models import User
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from django.conf import settings
from cryptography.hazmat.primitives import serialization
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .utils import verify_document_signature

# Web UI Views
def upload_document_view(request):
    if not request.user.is_authenticated or request.user.user_type != 'citizen':
        return redirect('login')
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            try:
                with open(settings.SERVER_KEY_PATH, 'rb') as key_file:
                    private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=None,
                        backend=default_backend()
                    )
                
                file_data = file.read()
                signature = private_key.sign(
                    file_data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                
                Document.objects.create(
                    owner=request.user,
                    file=file,
                    file_name=file.name,
                    digital_signature=signature.hex()
                )
                return redirect('download-document')
            
            except Exception as e:
                return render(request, 'documents/upload.html', {'error': str(e)})
    
    return render(request, 'documents/upload.html')

def download_document_view(request):
    if not request.user.is_authenticated or request.user.user_type != 'institution':
        return redirect('login')
    
    national_id = request.GET.get('national_id')
    documents = []
    if national_id:
        try:
            user = User.objects.get(national_id=national_id)
            documents = Document.objects.filter(owner=user)
        except User.DoesNotExist:
            pass
    return render(request, 'documents/download.html', {'documents': documents})

def download_file(request, document_id):
    if not request.user.is_authenticated or request.user.user_type != 'institution':
        return redirect('login')
    
    document = get_object_or_404(Document, id=document_id)
    is_valid = verify_document_signature(document, request.user, 'AUTO')
    
    if not document.file:
        raise Http404("Document not found")
    
    return FileResponse(document.file.open(), as_attachment=True, filename=document.file_name)

class UploadDocumentView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.user_type != 'citizen':
            return Response({"error": "Only citizens can upload documents"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            with open(settings.SERVER_KEY_PATH, 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
            
            file = request.FILES['file']
            file_data = file.read()
            
            signature = private_key.sign(
                file_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            document = Document(
                owner=request.user,
                file=file,
                file_name=file.name,
                digital_signature=signature.hex()
            )
            document.save()
            
            return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, national_id):
        if request.user.user_type != 'institution':
            return Response({"error": "Only institutions can download documents"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(national_id=national_id)
            documents = Document.objects.filter(owner=user)
            return Response(DocumentSerializer(documents, many=True).data)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
class VerifyDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, document_id):
        document = get_object_or_404(Document, id=document_id)
        is_valid = verify_document_signature(document, request.user, 'API')
        return Response({'is_valid': is_valid})
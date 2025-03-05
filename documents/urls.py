from django.urls import path
from .views import (
    upload_document_view,
    download_document_view,
    download_file,
    UploadDocumentView,
    DownloadDocumentView,
    VerifyDocumentView
)

urlpatterns = [
    path('upload/', upload_document_view, name='upload-document'),
    path('download/', download_document_view, name='download-document'),
    path('download/<int:document_id>/', download_file, name='download-file'),
    path('api/upload/', UploadDocumentView.as_view(), name='api-upload'),
    path('api/download/<str:national_id>/', DownloadDocumentView.as_view(), name='api-download'),
    path('api/verify/<int:document_id>/', VerifyDocumentView.as_view(), name='api-verify'),
]
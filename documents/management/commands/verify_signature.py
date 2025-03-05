from django.core.management.base import BaseCommand
from documents.models import Document
from documents.utils import verify_document_signature

class Command(BaseCommand):
    help = 'Verify document signature'

    def add_arguments(self, parser):
        parser.add_argument('document_id', type=int)

    def handle(self, *args, **options):
        doc = Document.objects.get(id=options['document_id'])
        result = verify_document_signature(doc)
        self.stdout.write(f"Document {doc.id} validity: {result}")
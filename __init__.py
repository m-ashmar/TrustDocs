# amn/__init__.py
from .cert_utils import generate_server_certificate
import os

def setup_certs():
    cert_dir = os.path.join(os.getcwd(), 'certs')
    if not os.path.exists(os.path.join(cert_dir, 'server_cert.pem')):
        generate_server_certificate()

# Call on Django startup
setup_certs()
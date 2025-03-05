# amn/cert_utils.py
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
import os

def generate_server_certificate():
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Generate CSR (Certificate Signing Request)
    csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"AMN-Server")])
    ).sign(key, hashes.SHA256())
    
    # Simulate CA signing (self-signed for development)
    cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u"CA-Server")])
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=0), critical=True
    ).sign(key, hashes.SHA256())
    
    # Save certificates
    cert_dir = os.path.join(os.getcwd(), 'certs')
    os.makedirs(cert_dir, exist_ok=True)
    
    # Save server certificate and key
    with open(os.path.join(cert_dir, 'server_cert.pem'), "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    with open(os.path.join(cert_dir, 'server_key.pem'), "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print("Server certificate and key generated in 'certs' directory!")
# AMN Document Management System 

A secure document management platform with digital signatures and role-based access control.

##  Features
###  Citizen Users:
- Upload documents with **RSA-2048** signatures.
- View upload history.

###  Institution Users:
- Search documents by **national ID**.
- Verify **digital signatures** for authenticity.

###  Security:
- **HTTPS/TLS 1.3 encryption** for secure data transfer.
- **Automatic certificate generation** for authentication.
- **Audit logging** for transparency and accountability.

---

##  Installation
***bash****
# Clone the repository
git clone https://github.com/m-ashmar/TrustDocs.git
cd amn-project

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser


 Development Mode
python manage.py runsslserver --cert certs/server_cert.pem --key certs/server_key.pem


 Production Mode (Recommended)
gunicorn --certfile=certs/server_cert.pem --keyfile=certs/server_key.pem amn.wsgi


 Security Architecture
Layer	Technology
Transport	TLS 1.3 + Let’s Encrypt
Authentication	JWT + Session Cookies
Storage	AES-256 Encrypted Files
Signatures	RSA-2048 + SHA-256



 Troubleshooting Tips 

SSL Certificate Errors

If you encounter SSL certificate issues, run the following command:
# Delete existing certificates and regenerate them
rm -rf certs/
python manage.py runserver

This will regenerate SSL certificates for secure communication.

------------------------------------------------
Developed with ❤️ by [m-ashmar]








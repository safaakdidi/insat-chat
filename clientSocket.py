import utils
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
def registerClientCertificateGen(siteName,country,state,local,orgName,email,certout,privateKeyout):
    csr = utils.createCertRequest(siteName,country,state,local,orgName,email,certout,privateKeyout)

    # Convert the CSR to a byte array
    csr_bytes = csr.public_bytes(serialization.Encoding.PEM)

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.56.102', 8001))

    # Send the CSR to the server
    client_socket.sendall(csr_bytes)
    print('csr sent')

    client_socket.shutdown(socket.SHUT_WR)

    cert_bytes = b''
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        cert_bytes += data
    print(cert_bytes)
    print('certif received')
    # #Convert the byte array to a certificate request object
    certificate = x509.load_pem_x509_certificate(cert_bytes, default_backend())
    print('certif received')
    print('*************')
    subject = certificate.subject
    print(subject)

    issuer = certificate.issuer
    print(issuer)
    # Extract the public key of the CSR
    public_key = certificate.public_key()
    print(public_key)

    # Extract the extensions of the CSR
    extensions = certificate.extensions
    for extension in extensions:
        print(extension)
    with open(certout, 'wb') as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    client_socket.close()
nom='safa'
email='safa@gmail.com'
num_card='123'
registerClientCertificateGen(nom,'TN', 'Tunis', 'insat',nom,email,f'build/{nom}{num_card}.cert',f'build/{nom}{num_card}.key')
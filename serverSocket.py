import socket,ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import utils
def registerClientCertificateSign():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.56.102', 8001))
    server_socket.listen(5)

    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

    # Receive the CSR from the client
    csr_bytes = b''
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        csr_bytes += data

    # Convert the byte array to a certificate request object
    csr = x509.load_pem_x509_csr(csr_bytes, default_backend())

    print('received')

    subject = csr.subject
    print(subject)

    # Extract the public key of the CSR
    public_key = csr.public_key()
    print(public_key)

    # Extract the extensions of the CSR
    extensions = csr.extensions
    for extension in extensions:
        print(extension)

    # create certificate
    certificate = utils.createCert(csr)
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

    cert_bytes = certificate.public_bytes(serialization.Encoding.PEM)

    print(cert_bytes)
    # Send the CSR signed to the client

    c = client_socket.sendall(cert_bytes)
    print(c)
    print('certificate sent')
    # Close the socket
    client_socket.close()
    server_socket.close()


registerClientCertificateSign()


# Host = "192.168.56.102"
# Port = 6390
#
# context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# context.load_cert_chain(certfile='build/server.cert',keyfile='build/server_private_key.key')
# context.load_verify_locations(cafile='build/serverCA.cert')
# context.verify_mode=ssl.CERT_REQUIRED
#
# bindsocket=socket.socket()
# bindsocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# bindsocket.bind(('', 10023))
# bindsocket.listen(5)
#
# newsocket,fromaddr=bindsocket.accept()
# connstream=context.wrap_socket(newsocket,server_side=True) #auth
# der=connstream.getpeercert(binary_form=True)
# client=x509.load_pem_x509_certificate(der,default_backend())
# print(client.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value)
# #create certificate for client
# utils.createCert(client)
#
# connstream.shutdown(socket.SHUT_RDWR)
# connstream.close()
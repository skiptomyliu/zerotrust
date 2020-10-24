
import boto3
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

kms = boto3.client('kms')
def decrypt_token(encrypted_blob, username):

    result = kms.decrypt(
    	KeyId = 'alias/vaulttesting',
    	CiphertextBlob=encrypted_blob,
    	EncryptionContext={
    		'username': username
    	}
    )
    return result['Plaintext']

def verify(token, username):
	blob = base64.b64decode(token)
	result = decrypt_token(encrypted_blob=blob, username=username)
	return result


class VerifyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        token = self.headers['x-ztrust-token']
        result = verify(token=token, username='dliu')
        self.wfile.write(result)


def run():
    print('starting server')
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, VerifyServer)
    print('running server')
    httpd.serve_forever()

run()
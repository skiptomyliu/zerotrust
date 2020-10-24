
import boto3
import base64
from botocore.exceptions import ClientError
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer


kms = boto3.client('kms')
def create_token(username):

    now = datetime.datetime.now()
    not_after = now + datetime.timedelta(minutes=60)
    not_before = now.strftime("%Y%m%dT%H%M%SZ")
    not_after = not_after.strftime("%Y%m%dT%H%M%SZ")

    plaintext = f'{{"not_before": "{not_before}", "not_after": "{not_after}"}}'

    result = kms.encrypt(
        KeyId = 'alias/vaulttesting',
        Plaintext=plaintext,
        EncryptionContext={
            'username': username
        }
    )
    return result['CiphertextBlob']


def decrypt_token(encrypted_blob):
    kms = boto3.client('kms')
    result = kms.decrypt(CiphertextBlob=encrypted_blob)
    return result['Plaintext']


class AgentServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        result = create_token(username='dliu')
        encoded = base64.b64encode(result)
        self.wfile.write(encoded)
        return

def run():
    print('starting agent')
    server_address = ('127.0.0.1', 8888)
    httpd = HTTPServer(server_address, AgentServer)
    print('running agent')
    httpd.serve_forever()


# result = create_token(username='dliu')
# encoded = base64.b64encode(result)

# plaintext = decrypt_token(base64.b64decode(encoded))
# print(plaintext)
run()



import boto3
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

import settings
kms = boto3.client("kms")


def decrypt_token(encrypted_blob, username):
    result = kms.decrypt(
        KeyId="alias/vaulttesting",
        CiphertextBlob=encrypted_blob,
        EncryptionContext={"username": username},
    )
    return result["Plaintext"]


def verify(token, username):
    blob = base64.b64decode(token)
    result = decrypt_token(encrypted_blob=blob, username=username)
    return result


class VerifyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.headers)

        try:
            token = self.headers["x-ztrust-token"]
            username = self.headers["x-ztrust-username"]
            result = verify(token=token, username=username)
            resp_code = 200
            resp_txt = b"ok"
            print(result)
        except Exception as e:
            print(e)
            resp_code = 403
            resp_txt = b"prohibited"

        self.send_response(resp_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(resp_txt)


def run():
    print("starting server")
    server_address = ("127.0.0.1", 8080)
    httpd = HTTPServer(server_address, VerifyServer)
    print("running server")
    httpd.serve_forever()


run()

import boto3
import base64
import datetime
import json
import requests

from http.server import BaseHTTPRequestHandler, HTTPServer

kms = boto3.client("kms")


def decrypt_token(encrypted_blob, username):
    result = kms.decrypt(
        KeyId="alias/vaulttesting",
        CiphertextBlob=encrypted_blob,
        EncryptionContext={"username": username},
    )
    return json.loads(result["Plaintext"])


def verify(token, username):
    blob = base64.b64decode(token)
    result = decrypt_token(encrypted_blob=blob, username=username)

    time_format = "%Y%m%dT%H%M%SZ"
    now = datetime.datetime.utcnow()
    not_before = datetime.datetime.strptime(result.get("not_before"), time_format)
    not_after = datetime.datetime.strptime(result.get("not_after"), time_format)

    return now < not_before or now > not_after

def authz(username):
    # request against OPA agent
    with open('./opa/data.json') as f:
        data = {}
        data['input'] = json.load(f)

    r = requests.post(
            'http://localhost:8181/v1/data/policy/allow',
            json=data,
            headers={'Content-type': 'application/json'}
        )
    return r.json()['result']


class VerifyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.headers)
        try:
            token = self.headers["x-ztrust-token"]
            username = self.headers["x-ztrust-username"]
            result = verify(token=token, username=username)
            if not result:
                raise Exception("Expired token")

            result = authz(username=username)
            if not result:
                raise Exception("Minimum Requirements not met.")

            resp_code = 200
            resp_txt = b"ok"
        except Exception as e:
            print(e)
            resp_code = 403
            resp_txt = str.encode(str(e))

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

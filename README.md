# zerotrust authn poc

![diagram](./images/diagram.png)

Note: This just contains the authn piece.  One of the largest missing pieces of 0-trust model is the usage of trust policies + trust engine.  This POC focuses on authn only.

Problem statement:
Be able to reach a domain (eg. `*.foobar.com`) without a VPN.

The following code in this repo has all components (except for KMS) to run locally on your computer.

## Chrome Extension
The extension acts as a client proxy where a listener is aded to look for requests made to foobar.com.  If a request is made to the domain, the extension will inject an encrypted token in the hTTP header.  It does this by calling the localhost agent where the agent is responsible for calling AWS KMS to create an encrypted token.

## Agent
The agent is only responsible for calling AWS KMS to create an encrypted token.

## AWS KMS
KMS is used by both the client and server.  The agent encrypts the token where the authn server decrypts the token.

### Client
User clients are only allowed to encrypt with an EncryptionContext set for their username.

```
"Condition": {
	"StringEquals": {
		"kms:EncryptionContext:username": "${aws:username}"
	},
	"Bool": {
		"aws:MultiFactorAuthPresent": "true"
        }
}
```

### Authnz Server
The server takes in the username and encrypted blob.  It uses the passed in username to match the encryption context.  If the authnz server is able to decrypt the token given the username, then we know the user is who they say they are.

## Envoy
Envoy acts as a front proxy.  We leverage the [Envoy authz filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter) to call an external HTTP endpoint for authn.

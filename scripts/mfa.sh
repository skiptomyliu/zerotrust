
acctcode=12345
user=username
echo "MFA Code"
read mfacode

result=`aws sts get-session-token --serial-number arn:aws:iam::$acctcode:mfa/$username --token-code $mfacode --profile=$username`
export AWS_ACCESS_KEY_ID=$(echo $result | jq -r .Credentials.AccessKeyId);
export AWS_SECRET_ACCESS_KEY=$(echo $result | jq -r .Credentials.SecretAccessKey);
export AWS_SESSION_TOKEN=$(echo $result | jq -r .Credentials.SessionToken)

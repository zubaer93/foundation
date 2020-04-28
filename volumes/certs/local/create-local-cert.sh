#!/usr/bin/env bash
set -eu
org=localhost-selfcertified

openssl genpkey -algorithm RSA -out "$1".key
openssl req -new -key "$1".key -out "$1".csr \
    -subj "/CN=$1/O=$org"

openssl x509 -req -in "$1".csr -days 365 -out "$1".crt \
    -CA ca.crt -CAkey ca.key -CAcreateserial \
    -extfile <(cat <<END
basicConstraints = CA:FALSE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
subjectAltName = DNS:$1
END
    )

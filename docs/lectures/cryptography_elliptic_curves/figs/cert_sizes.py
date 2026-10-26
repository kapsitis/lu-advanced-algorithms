# -*- coding: utf-8 -*-
"""Salīdzina RSA-2048, RSA-3072 un ECDSA P-256 sertifikātu ķēžu izmērus (12.6. uzdevums).

Katram algoritmam izveido mācību ķēdi "saknes CA -> starpniek-CA -> servera sertifikāts"
ar vienādiem nosaukumiem un paplašinājumiem un izdrukā DER izmērus baitos, kā arī
TLS 1.3 ziņojumu Certificate un CertificateVerify aptuveno izmēru.

    pip install cryptography
    python cert_sizes.py
"""

import datetime

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.x509.oid import NameOID


def new_key(alg):
    if alg == "P-256":
        return ec.generate_private_key(ec.SECP256R1())
    return rsa.generate_private_key(public_exponent=65537, key_size=int(alg.split("-")[1]))


def cert(subject, issuer, pub, issuer_key, ca, san=None):
    now = datetime.datetime(2026, 10, 1, tzinfo=datetime.timezone.utc)
    b = (x509.CertificateBuilder()
         .subject_name(x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, "LV"),
                                  x509.NameAttribute(NameOID.ORGANIZATION_NAME, "LU kursa piemers"),
                                  x509.NameAttribute(NameOID.COMMON_NAME, subject)]))
         .issuer_name(issuer)
         .public_key(pub)
         .serial_number(x509.random_serial_number())
         .not_valid_before(now)
         .not_valid_after(now + datetime.timedelta(days=3650 if ca else 90))
         .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True)
         .add_extension(x509.SubjectKeyIdentifier.from_public_key(pub), critical=False))
    if san:
        b = b.add_extension(x509.SubjectAlternativeName([x509.DNSName(s) for s in san]), critical=False)
    return b.sign(issuer_key, hashes.SHA256())


def chain(alg):
    root_k, int_k, leaf_k = new_key(alg), new_key(alg), new_key(alg)
    root_name = x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, "LV"),
                           x509.NameAttribute(NameOID.ORGANIZATION_NAME, "LU kursa piemers"),
                           x509.NameAttribute(NameOID.COMMON_NAME, "Piemera saknes CA")])
    root = cert("Piemera saknes CA", root_name, root_k.public_key(), root_k, True)
    inter = cert("Piemera starpniek-CA", root.subject, int_k.public_key(), root_k, True)
    leaf = cert("www.example.lv", inter.subject, leaf_k.public_key(), int_k, False,
                san=["www.example.lv", "example.lv"])
    if alg == "P-256":
        sig = leaf_k.sign(b"x" * 130, ec.ECDSA(hashes.SHA256()))
    else:
        sig = leaf_k.sign(b"x" * 130, padding.PSS(padding.MGF1(hashes.SHA256()), 32), hashes.SHA256())
    return root, inter, leaf, len(sig)


if __name__ == "__main__":
    print("%-8s %6s %6s %6s %6s %10s %10s" % ("alg", "SPKI", "sig", "leaf", "inter", "Cert.msg", "CertVerify"))
    for alg in ["RSA-2048", "RSA-3072", "P-256"]:
        root, inter, leaf, cv = chain(alg)
        spki = len(leaf.public_key().public_bytes(serialization.Encoding.DER,
                                                    serialization.PublicFormat.SubjectPublicKeyInfo))
        L, I = len(leaf.public_bytes(serialization.Encoding.DER)), len(inter.public_bytes(serialization.Encoding.DER))
        # Certificate ziņojums: 4 B galvene + 1 B konteksts + 3 B saraksta garums
        # + katram sertifikātam 3 B garums + 2 B (tukši) paplašinājumi; sakni nesūta
        msg = 4 + 1 + 3 + (3 + L + 2) + (3 + I + 2)
        print("%-8s %6d %6d %6d %6d %10d %10d" % (alg, spki, len(leaf.signature), L, I, msg, 4 + 2 + 2 + cv))

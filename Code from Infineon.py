from tpm2_pytss import *
from cryptography.hazmat.primitives import hashes

if __name__ == "__main__":
    # Initialize the ESAPI
    tpm = ESAPI()

    # Define the primary key sensitive data
    primary_sensitive = TPM2B_SENSITIVE_CREATE()

    # Create the primary key
    primary_handle, _, _, _, _ = tpm.create_primary(
        in_sensitive=primary_sensitive, in_public="rsa2048"
    )


    # Create the rsa key pair with primary key as parent
    # Define the rsa key sensitive data
    rsa_sensitive = TPM2B_SENSITIVE_CREATE()
    _, rsa_pub, _, _, _ = tpm.create(parent_handle=primary_handle, in_sensitive=rsa_sensitive, in_public="rsa2048")

    # Get the public part of the key in DER format
    rsa_pub_der = rsa_pub.to_der()

    hash_obj = hashes.Hash(algorithm=hashes.SHA256())
    hash_obj.update(rsa_pub_der)
    hash_digest = hash_obj.finalize().hex()
    print(hash_digest)

    tpm.close()

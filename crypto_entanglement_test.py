from tpm2_pytss import *
from cryptography.hazmat.primitives import hashes
import randtest as rt
import numpy
from nistrng import *

# Number of time to create the rsa key pair.
N = 5
percent_ipv61_rs = 0
percent_ipv62_rs = 0
percent_data_rs = 0
bigData = []
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
    for i in range(N):
        _, rsa_pub, _, _, _ = tpm.create(parent_handle=primary_handle, in_sensitive=rsa_sensitive, in_public="rsa2048")

        # Get the public part of the key in DER format
        rsa_pub_der = rsa_pub.to_der()
        print("T-" + str(N-i))
        hash_obj = hashes.Hash(algorithm=hashes.SHA256())
        hash_obj.update(rsa_pub_der)
        hash_digest = hash_obj.finalize().hex()
        #print(hash_digest)
        ipv61 = []
        ipv62 = []
        ipv61deci = []
        ipv62deci = []
        for i in range(0, 32, 4):
            # slicing into 4-character blocks starting at the first character
            ipv61.append(hash_digest[i: i + 4])
        for i in range(32, 64, 4):
            ipv62.append(hash_digest[i: i + 4])
        #print(ipv61)
        #print(ipv62)
        for i in range(0, 8):
            ipv61deci.append(int(ipv61[i], 16))
            ipv62deci.append(int(ipv62[i], 16))

        data = ipv61deci + ipv62deci
        print(data)
        data_arr = numpy.asarray(data)
        #print(data_arr)
        #binary_sequence: numpy.ndarray = pack_sequence(data_arr)
        #print(binary_sequence)
        # Check the eligibility of the test and generate an eligible battery from the default NIST-sp800-22r1a battery
        eligible_battery: dict = check_eligibility_all_battery(binary_sequence, SP800_22R1A_BATTERY)
        # Print the eligible tests
        print("Eligible test from NIST-SP800-22r1a:")
        for name in eligible_battery.keys():
            print("-" + name)
        # Test the sequence on the eligible tests
        results = run_all_battery(binary_sequence, eligible_battery, False)
        # Print results one by one
        print("Test results:")
        for result, elapsed_time in results:
            if result.passed:
                print("- PASSED - score: " + str(
                    numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(
                    elapsed_time) + " ms")
            else:
                print("- FAILED - score: " + str(
                    numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(
                    elapsed_time) + " ms")

        for i in range(0, len(data)):
            bigData.append(data[i])
        #print(bigData)
        data_rscore = rt.random_score(data)
        ipv61_rscore = rt.random_score(ipv61deci)
        ipv62_rscore = rt.random_score(ipv62deci)
        if ipv61_rscore == True:
            percent_ipv61_rs = percent_ipv61_rs + 1
        if ipv62_rscore == True:
            percent_ipv62_rs = percent_ipv62_rs + 1
        if data_rscore == True:
            percent_data_rs = percent_data_rs + 1

    tpm.close()
print("Number of iterations = " + str(N-1))
#print(percent_ipv61_rs / N)
#print(percent_ipv62_rs / N)
#print(percent_data_rs / N)
#print(rt.random_score(bigData))


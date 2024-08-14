from tpm2_pytss import ESAPI
from cryptography.hazmat.primitives import hashes
from tpm2_pytss import *
import numpy as np
from nistrng import *

N = 1000
passTimes = 0
failTimes = 0
totalScore = 0

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
        print("T-" + str(N-i))
        stringran = str(hash_digest)
        #print(stringran)
        #print(type(stringran))
        #print(len(stringran))
        bin_data = []
        for i in range(0, len(stringran), 2):
            # slicing into 2-character - 8-bits blocks - starting at the first character
            bin_data.append(stringran[i: i + 2])
        #print(bin_data)
        #print(len(bin_data))
        data = []
        for i in range(0, len(bin_data), 1):
            data.append(int(bin_data[i], 16))
        #print(data)
        # convert from a list to an array using numpy as-array
        data_arr = np.asarray(data, dtype=np.uint8)
        #print(data_arr)
        #print(data_arr.dtype)
        data_arr = data_arr.view(np.int8)
        data_arr -= 128
        print(data_arr)
        print(data_arr.dtype)
        binary_sequence: np.ndarray = pack_sequence(data_arr)
        print(binary_sequence)
        print(binary_sequence.dtype)
        print("Original sequence taken back by unpacking (to check the correctness of packing process:")
        print(unpack_sequence(binary_sequence))
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
                    np.round(result.score, 9)) + " - " + result.name + " - elapsed time: " + str(
                    elapsed_time) + " ms")
                passTimes += 1
                totalScore += result.score
            else:
                print("- FAILED - score: " + str(
                    np.round(result.score, 9)) + " - " + result.name + " - elapsed time: " + str(
                    elapsed_time) + " ms")
                failTimes +=1
                totalScore -= result.score
    tpm.close()
print("Number of iterations = " + str(N))
print("Pass Rate = " + str((passTimes-failTimes)*100/(passTimes+failTimes)) + " %")
print("Pass average score = " + str(totalScore/(passTimes+failTimes)))


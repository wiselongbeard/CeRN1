from tpm2_pytss import ESAPI
import randtest as rt
import numpy as np
from nistrng import *

N = 1
percent_data_rs = 0
bin_data = []
data = []
bigData = []
if __name__ == "__main__":
    # Initialize the Enhanced System API, aka "ESAPI"
    tpm = ESAPI()
    for i in range(N):
        # define the variable to hold the returned "TPM2B_DIGEST" of "32" random bytes
        # using the ESAPI.get_random function to invoke the TPM2_GetRandom command
        ran = ESAPI.get_random(self=tpm, bytes_requested=32)
        #print(ran)
        print("T-" + str(N-i))
        stringran = str(ran)
        print(stringran)
        print(type(stringran))
        print(len(stringran))
        bin_data = []
        for i in range(0, len(stringran), 2):
            # slicing into 2-character (8-bits) blocks starting at the first character
            bin_data.append(stringran[i: i + 2])
        print(bin_data)
        print(len(bin_data))
        for i in range(0, len(bin_data), 1):
            data.append(int(bin_data[i], 16))
        print(data)
        # convert from a list to a numpy array using np.asarray()
        data_arr = np.asarray(data, dtype=np.uint8)
        print(data_arr)
        print(data_arr.dtype)
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
            else:
                print("- FAILED - score: " + str(
                    np.round(result.score, 9)) + " - " + result.name + " - elapsed time: " + str(
                    elapsed_time) + " ms")

        for i in range(0, len(data)):
            bigData.append(data[i])
        #print(bigData)
        data_rscore = rt.random_score(data)
        if data_rscore == True:
            percent_data_rs = percent_data_rs + 1

    tpm.close()
print("Number of iterations = " + str(N-1))
print(percent_data_rs / N)
print(rt.random_score(bigData))

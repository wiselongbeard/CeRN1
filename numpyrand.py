import numpy
from nistrng import *

if __name__ == "__main__":
    # Generate the sequence of integers and pack it in its 8-bit representation
    sequence: numpy.ndarray = numpy.random.randint(-128, 128, 100, dtype=int)
    binary_sequence: numpy.ndarray = pack_sequence(sequence)
    # Print sequence
    print("Random sequence generated by NumPy:")
    print(sequence)
    print(sequence.dtype)
    print("Random sequence generated by NumPy encoded in 8-bit signed format:")
    print(binary_sequence)
    print(binary_sequence.dtype)
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
            print("- PASSED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
        else:
            print("- FAILED - score: " + str(numpy.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
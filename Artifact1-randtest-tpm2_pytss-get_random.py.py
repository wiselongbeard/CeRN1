from tpm2_pytss import ESAPI
import randtest as rt


N = 10001
percent_ipv61_rs = 0
percent_ipv62_rs = 0
percent_data_rs = 0
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
        #print(type(stringran))
        #print(len(stringran))
        ipv61 = []
        ipv62 = []
        ipv61deci = []
        ipv62deci = []
        for i in range(0, 32, 4):
            # slicing into 4-character blocks starting at the first character
            ipv61.append(stringran[i: i + 4])
        for i in range(32, 64, 4):
            ipv62.append(stringran[i: i + 4])
        #print(ipv61)
        #print(ipv62)
        for i in range(0, 8):
            ipv61deci.append(int(ipv61[i], 16))
            ipv62deci.append(int(ipv62[i], 16))

        data = ipv61deci + ipv62deci
        #print(data)
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
print(percent_ipv61_rs / N)
print(percent_ipv62_rs / N)
print(percent_data_rs / N)
print(rt.random_score(bigData))

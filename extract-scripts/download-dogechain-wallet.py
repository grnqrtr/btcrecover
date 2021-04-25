import http.client, sys, os.path, atexit, uuid

prog = os.path.basename(sys.argv[0])

if len(sys.argv) < 2:
    atexit.register(lambda: input("\nPress Enter to exit ..."))
    filename = "dogechain.wallet.aes.json"
elif len(sys.argv) == 2 and not sys.argv[1].startswith("-"):
    filename = sys.argv[1]
else:
    print("usage:", prog, "[NEW_DOGECHAIN_WALLET_FILE]", file=sys.stderr)
    sys.exit(2)

# Refuse to overwrite an existing file
assert not os.path.exists(filename), filename + " already exists, won't overwrite"

print("Please enter your wallet's ID (e.g. 9bb4c672-563e-4806-9012-a3e8f86a0eca)")
wallet_id = str(uuid.UUID(input("> ").strip()))

conn = http.client.HTTPSConnection("dogechain.info")

payload_preid = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"method\"\r\n\r\nget\r\n-----" \
          "011000010111000001101001\r\nContent-Disposition: form-data; name=\"guid\"\r\n\r\n"
payload_postid = "\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; " \
          "name=\"\"\r\n\r\n\r\n-----011000010111000001101001--\r\n"

headers = {
    'cookie': "__cfduid=debabd9ff80c97881979ab84beddd5c1f1619355025; request_method=POST",
    'Content-Type': "multipart/form-data; boundary=---011000010111000001101001"
    }

conn.request("POST", "/wallet/api", payload_preid + wallet_id + payload_postid, headers)

res = conn.getresponse()
data = res.read()

# Save the wallet
with open(filename, "wb") as wallet_file:
    wallet_file.write(data)

print("Wallet file saved as " + filename)
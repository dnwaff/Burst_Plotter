# add support for volume mounting

import ctypes
import os
import platform
import sys
import subprocess

multi_drive = True

def parse_filename(fname):
    acctid , nonce_offset , nonce_size , stagger = fname.split('_')
    return acctid , nonce_offset, nonce_size, stagger

def nonce_offset(offset , size):
    return int(offset) + int(size)

def max_nonce_offset():    
    max_nonce_offset = 0 
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        path = letter + ":\Burst\plots"
        if os.path.exists(path):
            files = os.listdir(path)
            for f in files:
                acctid, offset , size, stagger = parse_filename(f)
                local_offset = nonce_offset(offset, size)
                if local_offset > max_nonce_offset:
                    max_nonce_offset = local_offset
    return max_nonce_offset

def noncify(space_mb):
    OFFSET_GB = 10
    return ( (space_mb  / 1024) - OFFSET_GB) * 4096

def nonce_size(drive):
    path = drive + "Burst\plots"

    space_mb = get_free_space_mb(drive)

    nonce_size = noncify(space_mb)

    return nonce_size
    
def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024

def err(text):
    print text
    quit()

def plot_file(acctid = 12222039840188650036 , drive = "G:/" , stagger = 4096 ):

    if not os.path.exists(drive):
        err("bad path")
        
    size = nonce_size(drive)

    if size < 10000:
        err("don't bother")

    offset = 0

    if multi_drive:
        offset = max_nonce_offset()

    cmd = "gpuPlotGenerator generate buffer " + drive + str(acctid) + "_" + str(offset) + "_" + str(size) + "_" + str(stagger)

    cmd_path = "C:\Users\Darryl\Downloads\GpuPlotGenerator"

    print cmd_path + " " + cmd

    os.chdir(cmd_path)
    
    print os.system(cmd)


# if plot file fails . run plot checker. if ok, get nonce where we left off from at drive
# if plot bad, start all over. AKA use burst plots folder

def plot_checker(plot_path):
    cmd_path = "C:\\"

    os.chdir(cmd_path)

    cmd = "PlotsChecker.exe " + plot_path

    p1 = subprocess.Popen(cmd , stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    stdout , stderr = p1.communicate()

    print stdout

    #print os.system( cmd )

    
plot_file(drive = "G:/")

#plot_checker("G:/")

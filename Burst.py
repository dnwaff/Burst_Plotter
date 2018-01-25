# add support for volume mounting

import ctypes
import os
import platform
import string


def parse_filename(fname):
    file_info = fname.split("_")
    acctid = 0
    nonce_offset = 0
    nonce_size = 0
    stagger = 0

    if len(file_info) == 4:
        acctid, nonce_offset, nonce_size, stagger = file_info
    return acctid, nonce_offset, nonce_size, stagger

def nonce_offset(offset, size):
    return int(offset) + int(size)

def get_drives():
    drive_list = []
    for letter in string.ascii_uppercase.replace("C",""):
        path = letter + ":\\"
        drive_list.append(path)

    return drive_list

def max_nonce_offset(id):
    max_nonce_offset = 0
    for drive in get_drives():
        path = drive + "Burst\plots"
        if os.path.exists(path):
            files = os.listdir(path)
            for f in files:
                acctid, offset, size, stagger = parse_filename(f)
                if acctid != id:
                    continue
                local_offset = nonce_offset(offset, size)
                if local_offset > max_nonce_offset:
                    max_nonce_offset = local_offset
    return max_nonce_offset


def noncify(space_mb):
    # OFFSET_GB = 10
    return ((space_mb / 1024)) * 4096

def has_plots(drive , id):
    path = drive + "Burst\plots"
    if os.path.exists(path):
        files = os.listdir(path)
        for f in files:
            acctid = parse_filename(f)[0]
            if acctid == id:
                return True
    return False

def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize / 1024 / 1024


def nonce_size(drive):
    space_mb = get_free_space_mb(drive)

    nonce_size = noncify(space_mb)

    return nonce_size


def err(text):
    print text
    quit()

from Burst import *
from Plotter import Plotter
from PlotChecker import PlotChecker
import os
import filecmp
from ContexManager import cd


# if plot file fails . run plot checker. if ok, get nonce where we left off from at drive
# if plot bad, start all over. AKA use burst plots folder

def run():

    drive , multi_drive =  _  , _

    size = nonce_size(drive)

    if size < 10000:
        print "don't bother"

    offset = 0

    if multi_drive:
        offset = max_nonce_offset()






def plot(acctid='12222039840188650036', offset=0, stagger=4096):
    offset = max_nonce_offset(acctid)
    drives = get_drives()
    for drive in drives:
        if os.path.exists(drive):
            if has_plots(drive, acctid) and nonce_size(drive) < 3750000*(0.7): # approx 1000GB
                continue
            else:
                size = nonce_size(drive)
                print "plotting ", drive , acctid , offset, size, stagger
                Plotter().run(drive, acctid, offset, size, stagger)
                offset = offset + size




def plot_drives(acctid='12222039840188650036', offset=0, drives=[], stagger=4096):
    p_offset = offset
    if not isinstance(drives, list):
        drives = [drives]
    for drive in drives:
        if not os.path.exists(drive):
            print "not a valid drive, continuing to next drive"
            continue


        size = nonce_size(drive)

        Plotter().run(drive, acctid, p_offset, size, stagger)

        p_offset = nonce_offset(p_offset, size)

    print "finished"


def move_plot(plot_path, acctid):
    if os.path.exists(plot_path):
        files = os.listdir(plot_path)
        for f in files:
            id = parse_filename(f)[0]
            if id != acctid:
                continue

            with(plot_path):
                command = "move " + f + " " + plot_path + "Burst\plots"
                print command
                os.system(command)
                print "move file " + f




#plot_drives(acctid ='12222039840188650036', offset = '129101824' , drives = ["J:\\","K:\\"], stagger = 4096)
#plot(acctid ='12222039840188650036')
#print nonce_offset(max_nonce_offset('12222039840188650036'), "30519296")
for letter in string.ascii_uppercase.replace("C",""):
    if os.path.exists(letter + ":\Burst\plots"):
        print "checking: ", letter + ":\Burst\plots"
        PlotChecker().check(letter + ":\Burst\plots")
#move_plot("H:\\",'12222039840188650036')


#print filecmp.cmp('gen_out.log', 'program/test.log')


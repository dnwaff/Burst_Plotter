import subprocess
import threading
import os
import sys
from shutil import copyfile
import time
import filecmp
from ContexManager import cd


def read_last():
    with open('..\gen_out.log', "r+") as log:
        content = log.readlines()
    my_line = []
    for line in content:
        my_line.append(line.replace('\x08', ''))

    lines = my_line[-1].split('...')
    print lines[-2].strip()




class PlotCommand(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.checker_thread = None

    def run(self, timeout):

        def checker(process):
            timeout_cntr = 0
            output_log = '..\gen_out.log'
            copyfile(output_log, "test.log")
            while process.poll() is None:
                time.sleep(60)



                if filecmp.cmp(output_log, "test.log"):
                    timeout_cntr = timeout_cntr + 1
                    print "timing out at count 6. current count: ",timeout_cntr
                else:
                    timeout_cntr = 0
                    copyfile(output_log, "test.log")
                    read_last()

                if timeout_cntr > 1000000000:
                    print "terminating"
                    process.terminate()
                    break





        def target():
            print 'Thread started'
            output_log = '..\gen_out.log'
            checker_thread = None
            with open(output_log, "wb") as log:
                self.process = subprocess.Popen(self.cmd, shell=False, stdout= log)
                checker_thread = threading.Thread(target = checker, args = (self.process,))
                checker_thread.daemon= True
                checker_thread.start()
                self.process.communicate()



            # while True:
            #     out = self.process.stdout.read(1)
            #     if out == '' and self.process.poll() != None:
            #         break
            #     if out != '':
            #         sys.stdout.write(out)
            #         sys.stdout.flush()

            print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join()



        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()
        print self.process.returncode

class Plotter:

    def __init__(self):
        pass

    def run(self, drive , acctid=12222039840188650036, offset= 0 , size = 0 , stagger=4096):

        if not os.path.exists(drive):
            print "bad path"
            return -1

        cmd = "gpuPlotGenerator.exe generate buffer " + drive + str(acctid) + "_" + str(offset) + "_" + str(size) + "_" + str(stagger)

        cmd_path = "program\\"

        print cmd_path + cmd

        with cd(cmd_path):
            t = PlotCommand(cmd)
            t.run(timeout= -1)

        return 1



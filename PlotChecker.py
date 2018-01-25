import subprocess
import ContexManager

class PlotChecker():

    def __init__(self):
        pass

    def check(self, plot_path):
        cmd_path = "program\\"

        cmd = cmd_path + "PlotsChecker.exe " + plot_path


        p1 = subprocess.Popen(cmd , stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        stdout , stderr = p1.communicate()

        print stdout
from subprocess import Popen, PIPE
import re
IP = "192.168.0.15"




def get_mac_address(ip):
    pid = Popen(["arp", "-n", ip], stdout = PIPE)
    s = pid.communicate()[0]
    mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]

    return mac
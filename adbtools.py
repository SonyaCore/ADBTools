#!/usr/bin/env python3

import subprocess  , sys
import time
from simple_term_menu import TerminalMenu

__author__ = "Sonia Core"
__email__ = "####"
__license__ = "GPL-3"
__version_info__ = (0, 0, 2)
__version__ = ".".join(map(str, __version_info__))


BANNER = """
   __    ____  ____    ____  _____  _____  __    ___ 
  /__\  (  _ \(  _ \  (_  _)(  _  )(  _  )(  )  / __)
 /(__)\  )(_) )) _ <    )(   )(_)(  )(_)(  )(__ \__ \\
(__)(__)(____/(____/   (__) (_____)(_____)(____)(___/

"""

BANNEDWORDS = ["localhost", "127.0.0.1"]
ADBPORT = ":5555"
MODES = ["Connect" , "Disconnect", "Reset Connection" , "Turn on Wifi"]
WIFI = ["disable" , "enable"]

class IPParser(object):
   def validIPAddress(self, IP):
      """
      :type IP: str
      :rtype: str
      """
      def isIPv4(s):
         try: return str(int(s)) == s and 0 <= int(s) <= 255
         except: return False
      def isIPv6(s):
         if len(s) > 4:
            return False
         try : return int(s, 16) >= 0 and s[0] != '-'
         except:
            return False
      if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
         "IPv4"
         return True
      if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
         "IPv6"
         return True
      
      return False

def proc_executer(argument : list) :
    return subprocess.run(
    argument, capture_output=True, text=True)

def router_stat() -> list:
    ip_parse = IPParser()
    result = proc_executer(["netstat", "-r", "-f", "inet"])

    lines: list = result.stdout.strip().split("\n")
    
    raw_ip_addresses: list = []
    ips: list = []

    #####
    for line in lines:
        columns = line.strip().split()
        if len(columns) >= 2:
            raw_ip_addresses.append(columns[1])

    for ip in raw_ip_addresses:
        if ip in (BANNEDWORDS):
            pass

        elif ip_parse.validIPAddress(ip):
            ips.append(ip)
    #####
    return ips


def cmd_adb_connection(method : str , ip: str, port: str = ADBPORT) -> None:
    if method == "connect" :
        proc_executer(["adb" , "tcpip" ,ADBPORT.replace(":","")])
        cmd = proc_executer(["adb", "connect", ip + port])
    elif method == "disconnect" :
        cmd = proc_executer(["adb", "disconnect", ip + port])

    result : str = cmd.stdout.strip()
    print(result)


def cmd_connection_reset() -> None:
    proc_executer(['adb','shell','cmd' ,'connectivity' ,'airplane-mode' , 'enable'])
    time.sleep(1.0)
    proc_executer(['adb','shell','cmd' ,'connectivity' ,'airplane-mode' , 'disable'])
    time.sleep(1.0)
    proc_executer(['adb','shell' ,'svc', 'data' ,'enable'])
    
    

def cmd_wifi(value : str) -> None:
    proc_executer(['adb','shell' ,'svc' ,'wifi' ,value])

###########################
def main():
    print(BANNER)
    print("ADB Tools" , __version__)
    print("Python" , sys.version , sys.platform)
    options = router_stat()

    ### Menu entry
    terminal_menu_mode = TerminalMenu(MODES)
    terminal_menu_mode.show()
    val = terminal_menu_mode.chosen_menu_index
    
    if val == 0 :
        adb_method = "connect"
    elif val == 1:
        adb_method = "disconnect"

    if val in (0 , 1):
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()

        ### exec con mode
        cmd_adb_connection(adb_method , options[menu_entry_index])

    elif val == 2:
        cmd_connection_reset()

    elif val == 3 :
        wifi_menu = TerminalMenu(WIFI)
        wifi_val = wifi_menu.show()
        cmd_wifi(WIFI[wifi_val])

        
    else :
        exit(1)
    
###########################
if __name__ == "__main__":
    main()

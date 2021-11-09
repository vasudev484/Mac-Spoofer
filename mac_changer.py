#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguements():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface", dest = "interface", help = "Interface that needs the MAC change")
    parser.add_option("-m", "--mac", dest = "new_mac", help = "New MAC address")
    (options, arguements) = parser.parse_args()
    if not options.interface:
        #error message
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_addr_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_addr_result:
        return mac_addr_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguements()
current_mac = get_current_mac(options.interface)
print("Current MAC: " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was changed to " + current_mac + ".")
else:
    print("[-] MAC address did not change.")

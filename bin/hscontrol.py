from homeseerpy import HomeseerPy
import sys
import os
from prettytable import PrettyTable

def main():

    #**** CHANGE THIS TO YOUR HOMESEER SERVER IP ADDRESS ****

    #hs = HomeseerPy("http://192.168.10.102","USERNAME","PASSWORD")
    hs = HomeseerPy("http://192.168.10.102")

    #**** CHANGE THIS TO YOUR HOMESEER SERVER IP ADDRESS ****

    if len(sys.argv) == 1:
        #clear screen first
        os.system('cls' if os.name == 'nt' else 'clear')
        print '''
        To control an HS device supporting on/off/dim then enter the
        following:

        On   :\thousecode on
        Off  :\thousecode off
        DDim :\thousecode ddim level (dims to absolute dim value)
        Dim  :\thousecode dim level (dims relative to current level)

        example :\tB10 ddim 10
        \t\tB10 on

        To set the string of a device such as as virtual device supporting
        Play/Pause/Stop any other status bit enter the following:

        string housecode status_string
        or
        s housecode status_string

        example :\tstring B10 Stopped
        \t\tsB10 Connected

        To obtain the status of a Homeseer interface pass the interface
        name as the first argument. If your string has spaces be sure to
        enclose it in quotes such as "Motion Detectors". Homeseer IS case
        sensitive so keep this in mind. "zwave" is NOT equivalent to "ZWave"

        example: \t ZWave
        \t\t "Motion Detectors"

        ** DON'T FORGET TO CHANGE THE URL PARAMETER IN THE SCRIPT **
        ** TO MATCH THE IP ADDRESS OF YOUR HOMESEER SERVER        **
        '''
        sys.exit(0)

    def run_control(command):
        results = hs.control(command, device_housecode, device_command,
                             dim_level)
        print '''
        Your string was    :\t%s
        Your housecode was :\t%s
        Your command was   :\t%s
        Your options were  :\t%s ''' \
            % (command, device_housecode, device_command, dim_level[1:])
        print ("Response : " + results)

    def run_status(command):
        results = hs.status(command)
        #clear screen first
        os.system('cls' if os.name == 'nt' else 'clear')

        #iterate through list. Return only the rows we want which are :
        #Status, Name, Last Changed.
        #Limit the second row "Name" to be no more than 35 characters +
        #two ".." for proper screen formatting on an 80 row wide terminal
        #for items in results:
        #    print str(items[0]).ljust(20) +  \
        #        str(items[2][:35] + (items[2][35:]
        #            and '..')).ljust(39) + str(items[5])

        #print hs.createdict(results)
        #print hs.createjson(results)

        x = PrettyTable([results[0][0], results[0][2], results[0][5]])
        x.align[results[0][0]] = "l"
        results.pop(0)
        x.padding_width = 1
        for items in results:
            x.add_row([items[0], items[2], items[5]])
        print x
        
    commandline = sys.argv[1]

    if 1 < len(commandline) <= 3 and commandline != 'All':
        device_housecode = sys.argv[1]
        device_command = str.lower(sys.argv[2])
        if sys.argv[3:]:
            dim_level = ",%s" % (sys.argv[3])
        else:
            dim_level = ''
        run_control("exec")

    elif len(commandline) == 1 and commandline == 's':
        device_housecode = sys.argv[2]
        device_command = (sys.argv[3]).title()
        dim_level = ''
        run_control("string")

    elif sys.argv[2:3]:
        device_housecode = sys.argv[2]
        device_command = str.lower(sys.argv[3])
        if sys.argv[4:]:
            dim_level = ",%s" % (sys.argv[4])
        else:
            dim_level = ''
        run_control(commandline)

    else:
        interface = sys.argv[1]
        run_status(interface)

if __name__ == "__main__":
    main()

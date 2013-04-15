#A basic Homeseer control base class.

###INSTALLATION : `install 'python setup.py install'`

####Usage:
 `from homeseerpy import HomeseerPy`  
 `hs = HomeseerPy("IPADDRESS"[, username="username", password"pass"])`  

If running the hscontrol.py command line script then a configuration file  
must be created in the user's home directory. The file should be named  
'.hscontrol.cfg' and contain the following:  

hostname your_hs_ip_or hostname (without trailing http://)  
username your_hs_username  
password your_hs_password  

####Implemented functions:
___control___: to control Homeseer interfaces  
___status___: to display the current status interfaces

To control an HS device supporting on/off/dim then enter the following:

    On   : exec housecode on
    Off  : exec housecode off
    DDim : exec housecode ddim level (dims to absolute dim value)
    Dim  : exec housecode dim level (dims relative to current level)

    example : exec B10 ddim 10
              exec B10 on

To set the string of a device such as as virtual device supporting
Play/Pause/Stop any other status bit enter the following:

    string housecode status_string

    example : string B10 Stopped
              string B10 Connected

To obtain the status of a Homeseer interface pass the interface name as the
first argument. If your string has spaces be sure to enclose it in quotes
such as "Motion Detectors". Homeseer IS case sensitive so keep this in mind.
zwave is NOT equivalent to ZWave.

    example: ZWave
             "Motion Detectors"

When calling from the command line the script assumes the default command if
passed a Housecode is 'exec' so it's not required. A device string can be set using the command 's'.

    To turn on/off a device:
                             B10 on 
                             B10 off
                             
    To dim a device to a specific level:                                    
                                        B10 dim 30 (dims relative to current value on supported devices)
                                        B10 ddim 30 (dims to absolute dim value)
                                        
    To set the device string:
                             s B10 "Now Playing"
                             s B10 "Connected"
    

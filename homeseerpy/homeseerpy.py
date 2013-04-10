'''
A basic Homeseer control base class.

Usage: [ ] denotes optional arguments
 - from homeseerpy import HomeseerPy
     hs = HomeseerPy("IPADDRESS"[, username="username", password"pass"])

Implemented functions
 - control:
        to control Homeseer interfaces
 - status:
        to display the current status interfaces

TODO:
 - implement more robust control and status. Hopefully be able to manage
 entire HS setup from Python.
'''
__version__ = "0.6"

import requests
import time
import lxml
import lxml.html
import json
#import itertools

class HomeseerPy(object):

    ''' Homeseer base class.
    Requires the Homeseer base URL or IP address passed to init.

    Usage: [ ] denotes optional arguments

    -from homeseerpy import HomeseerPy
         hs = HomeseerPy("IPADDRESS"[, username="username", password"pass"])


    To control an HS device supporting on/off/dim then enter the following:

        On   :exec housecode on
        Off  :exec housecode off
        DDim :exec housecode ddim level (dims to absolute dim value)
        Dim  :exec housecode dim level (dims relative to current level)

        example :exec B10 ddim 10
                 exec B10 on

    To set the string of a device such as as virtual device supporting
    Play/Pause/Stop any other status bit enter the following:

        string housecode status_string

        example :string B10 Stopped
                 string B10 Connected

    To obtain the status of a Homeseer interface pass the interface name as
    the first argument. If your string has spaces be sure to enclose it in
    quotes such as "Motion Detectors". Homeseer IS case sensitive so keep
    this in mind. "zwave" is NOT equivalent to "ZWave."

        example: ZWave
                 "Motion Detectors"
    '''

    def __init__(self, url, username='', password=''):
        self.url = url
        self.username = username
        self.password = password

    def control(self, script_command, device_housecode,
                device_command, dim_level=''):
        '''To control an HS device supporting on/off/dim then enter
         the following:

        Usage:
        hs.control(exec, B10, on)

        On   :exec housecode on
        Off  :exec housecode off
        DDim :exec housecode ddim level (dims to absolute dim value)
        Dim  :exec housecode dim level (dims relative to current level)

        example :exec B10 ddim 10
                 exec B10 on

        To set the string of a device such as as virtual device supporting
        Play/Pause/Stop any other status bit enter the following:

        string housecode status_string

        example :string B10 Stopped
                 string B10 Connected
        '''

        if str.lower(script_command) == "exec":
            script_command = "execx10"
        elif str.lower(script_command) == "string":
            script_command = "setdevicestring"

        payload = {'devlist': '0', 'dev_value': '', 'devaction': '',
                'delay_hours': '0', 'delay_minutes': '0', 'delay_seconds': '0',
                'message': '', 'hosts': '', 'runscript': 'Execute+Command',
                'ref_page': 'ctrl', 'scriptcmd': '&hs.%s("%s","%s"%s)'
                % (script_command, device_housecode, device_command,
                   dim_level)}

        try:
            website = requests.post(self.url, data=payload, auth=
                                    (self.username, self.password),
                                        timeout=2)
            website.close()

        except requests.exceptions.ConnectionError as detail:
            raise requests.exceptions.ConnectionError\
            ("Could not connect to server. Check that\
            Homeseer is running and that the ip address is correct."\
            , detail)

        #wait 1 second before checking status as it takes a moment
        #for HS to update
        time.sleep(1)

        #Connect to Homeseer and open the log file.
        try:
            website = requests.get(self.url + "/elog", auth=
                                   (self.username, self.password), timeout=2)
            website.close()

        except requests.exceptions.ConnectionError as detail:
            raise requests.exceptions.ConnectionError\
            ("Could not connect to server. Check that\
            Homeseer is running and that the ip address is correct."\
            , detail)

        tree = lxml.html.fromstring(website.content)
        #Search for the latest log entry '''
        elements = tree.xpath("//td[@class='LOGEntry0']")
        results = elements[0].text_content()

        return results

    def status(self, script_command):
        '''To obtain the status of a Homeseer interface pass the interface
        name as the first argument. If your string has spaces be sure to
        enclose it in quotes such as "Motion Detectors". Homeseer IS case
        sensitive so keep this in mind. "Zwave" is NOT equivalent to "ZWave"

        Usage:
        hs.status("ZWave")

        example: ZWave
                 "Motion Detectors"
        '''

        url = self.url + "/stat?location=" + script_command

        try:
            website = requests.get(url, auth=(self.username, self.password),
                                   timeout=2)
            website.close()

        except requests.exceptions.ConnectionError as detail:
            raise requests.exceptions.ConnectionError\
            ("Could not connect to server. Check that\
            Homeseer is running and that the ip address is correct."\
            , detail)

        tree = lxml.html.fromstring(website.content)
        #parse xpath and retrieve appropriate tables
        elements = tree.xpath("\
        //td[contains(@class, 'table') and not (contains(@id, 'dx')) \
        and not (contains(@class, 'tableheader')) \
        and not (contains(form/@name, 'statform')) \
        and not (contains(text(), 'Control'))]//text()\
        [normalize-space()]")

        #function to split lists into chunks of (x) size '''
        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

        #strip all line feeds
        output = []
        for i in elements:
            output.append(i.strip())

        #call chunker function and output lists of 6 as that's how many rows
        #Homeseer has.
        results = []
        for group in chunker(output, 6):
            results.append(group)

        return results

    def createdict(self, data):
        ''' Create a dict with the results scraped from Homeseer.
        Keys are "Status", "Name", "Interface", "Housecode", "Type",
        and "Last Changed"
        '''
        dresults = []
        data_iter = iter(data)
        data_header = data_iter.next()
        for row in data_iter:
            dresults.append(dict(zip(data_header, row)))
        return dresults

    def createjson(self, data):
        ''' Creates a JSON tree from a dictionary(self.createdict) with
        the results scraped from Homeseer. Returns "Status", "Name", 
        "Interface", "Housecode", "Type", and "Last Changed"
        '''
        jresults = json.dumps(self.createdict(data), indent=4, separators=(',', ': '))
        return jresults

    #def grouper(n, iterable, fillvalue=None):
        #"grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        #args = [iter(iterable)] * n
        #return izip_longest(fillvalue=fillvalue, *args)

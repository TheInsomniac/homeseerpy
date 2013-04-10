from nose.tools import * 
from homeseerpy.homeseerpy import HomeseerPy
import time

def test_status():
    hs = HomeseerPy("http://192.168.10.102")
    hs.status("ZWave")

def test_control():
    hs = HomeseerPy("http://192.168.10.102")
    hs.control("exec", "q1", "on")
    time.sleep(2)
    hs.control("exec", "q1", "off")


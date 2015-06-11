#!/usr/bin/python
'''
Usage::

    ./decoder.py [module] [data_file]

Sample::

    ./decoder.py pyroute2.netlink.rtnl.tcmsg.tcmsg ./sample_packet_01.data
    ./decoder.py pyroute2.netlink.nl80211.nl80211cmd ./nl80211.data

Module is a name within rtnl hierarchy. File should be a
binary data in the escaped string format (see samples).
'''
import io
import sys
from pprint import pprint
from importlib import import_module

mod = sys.argv[1]
f = open(sys.argv[2], 'r')
b = io.BytesIO()
s = mod.split('.')
package = '.'.join(s[:-1])
module = s[-1]
m = import_module(package)
met = getattr(m, module)


for a in f.readlines():
    if a[0] == '#':
        continue
    if a[0] == '.':
        break
    while True:
        if a[0] == ' ':
            a = a[1:]
            continue
        try:
            b.write(chr(int(a[2:4], 16)))
        except:
            break
        a = a[4:]

b.seek(0)
data = b.getvalue()

offset = 0
inbox = []
while offset < len(data):
    msg = met(data[offset:])
    msg.decode()
    pprint(msg)
    offset += msg['header']['length']

# An example how to use command chaining in IPDB

from pyroute2 import IPDB

with IPDB() as ip:
    # create bonding
    ip.create(ifname='bo0', kind='bond', bond_mode=2).commit()
    # create slave ports
    ip.create(ifname='bo0p0', kind='dummy').commit()
    ip.create(ifname='bo0p1', kind='dummy').commit()
    # set up bonding
    ip.interfaces.bo0.add_port(ip.interfaces.bo0p0).\
        add_port(ip.interfaces.bo0p1).\
        add_ip('172.16.0.1/24').\
        add_ip('172.16.0.2/24').\
        option('mtu', 1400).\
        up().\
        commit()

    for i in ('bo0p0', 'bo0p1', 'bo0'):
        try:
            ip.interfaces[i].remove().commit()
        except:
            pass

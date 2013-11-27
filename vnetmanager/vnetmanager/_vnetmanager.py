#!./flask/bin/python

DEBUG = False

class HostNotFoundError(Exception):
    def __init__(self, mac):
        self.value = "Host with MAC %s could not be found" % mac

    def __str__(self):
        return repr(self.value)

class vNetUser:
    def __init__(self):
        self.userid = None      # INTEGER AUTO-INCREMENT
        self.username = None    # VARCHAR(20)
        self.password = None    # VARCHAR(20)

        self.authroizedNetworks = []


class IpConfiguration:
    def __init__(self, prefix, cidr):
        self.prefix = prefix    # VARCHAR(15)
        self.cidr = cidr        # INTEGER


class NetworkSwitch:
    def __init__(self, dpid, neighbors = {}):
        self.dpid = dpid                    # CHAR(23)
        self.neighbors = neighbors   
        self.vlanToPort = {}


    def addflows(self, port, mac, vnet):

        vlan = vnet.vlan
        outtable = vlan

        if vlan not in self.vlanToPort.keys():
            self.vlanToPort[vlan] = []

        self.vlanToPort[vlan].append(port)


        inflowstr = "table=0, priority=100, in_port=%d, vlan_tci=0, " \
                  + "dl_src=%s, actions=mod_vlan_vid:%d,resubmit(,%d)" \
                  % (port, mac, vlan, outtable)

        outflowstr = "table=%d, priority=100, dl_vlan=%d, dl_dst=%s, " \
                   + "actions=strip_vlan,output:%d" \
                   % (outtable, vlan, mac, port)


        fo = open("/tmp/flow", "wb")
        fo.write("%s\n%s\n%s" % (inflowstr, outflowstr, self.broadcast(vnet, outtable)))
        fo.close()
        subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', self.dpid, '/tmp/flow'])


    def broadcast(self, vnet, outtable):
        flowstr = "table=%d, priority=101,dl_vlan=%d, dl_dst=ff:ff:ff:ff:ff:ff, " \
                + "actions=strip_vlan,output:" \
                % (outtable, vnet.vlan)

        for port in self.vlanToPort[vnet.vlan]: 
            flowstr += "%d," % port
        
        '''
        fo = open("/tmp/flow", "wb")
        fo.write(flowstr)
        fo.close()
        subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', self.server, '/tmp/flow'])
        '''
        return flowstr



class Network:
    def __init__(self, ipconf, hosts = {}):
        self.ipconf = ipconf
        self.hosts = hosts

    def addHost(self, h):
        # TODO: Verify that h.ip exists within range specified by ipconf
        self.hosts[h.mac] = h
        return self

    def removeHost(self, mac):
        return self.hosts.pop(mac)


class PhysicalNetwork(Network):
    def __init__(self, ipconf, hosts = {}, switches = {}):
        Network.__init__(self, ipconf, hosts)
        self.switches = switches
        self.switchLinks = []
        self.hostLinks = {}

    def addSwitch(self, sw):
        self.switches[sw.dpid] = sw
        return self

    def addSwitches(self, swlist):
        for sw in swlist:
            self.switches[sw.dpid] = sw

        return self

    def removeSwitch(self, dpid):
        for (link, cost) in self.switchLinks:
            ((sw0dpid, sw0port), (sw1dpid, sw1port)) = link
            if dpid in [sw0dpid, sw1dpid]:
                self.removeSwitchLink(link)

        return self.switches.pop(dpid)

    def addSwitchLink(self, link, cost = 1):
        ((sw0dpid, sw0port), (sw1dpid, sw1port)) = link
        if not (sw0dpid in self.switches.keys() and sw1dpid in self.switches.keys()):
            raise Exception("%s, %s, or both are invalid switch IDs" % (sw0dpid, sw1dpid))

        if (link, cost) in self.switchLinks:
            self.switchLinks.remove((link, cost))

        self.switchLinks.append((link, cost))

        return self


    def removeSwitchLink(self, link):
        return self.switchLinks.pop(link)


class VirtualNetwork(Network):
    def __init__(self, ipconf, vNetID, vlan, hosts = {}):
        Network.__init__(self, ipconf, hosts)
        self.vNetID = vNetID
        self.vlan = vlan


class NetworkHost:
    def __init__(self, mac, ip):
        self.mac = mac
        self.ip = ip


class VirtualNetworkHost(NetworkHost):
    # def __init__(self, mac, ip, physicalHost):
    def __init__(self, physicalHost):
        NetworkHost.__init__(self, mac, ip)
        self.physicalHost = physicalHost


class PhysicalNetworkHost(NetworkHost):
    def __init__(self, mac, ip, user, accessLink):
        NetworkHost.__init__(self, mac, ip)
        self.user = user
        self.accessLink = accessLink
        self.virtualHosts = {}


class AccessLink:
    def __init__(self, sw, swport):
        self.switch = sw
        self.port = swport


class NetworkSwitch:
    def __init__(self, dpid):
        self.dpid = dpid
        self.neighbors = {}
        self.routes = {}
        self.flows = []

    def addNeighbor(self, neigh, swport):
        for (n_dpid, (n, sp)) in neighbors.iteritems():
            if sp == swport:
                msg = "Switch %s alread has a neighbor at port %d: %s"
                raise Exception(msg % (self.dpid, sp, n_dpid))

        self.neighbors[neigh.dpid] = (neigh, swport)
        return self


    def removeNeighbor(self, neigh):

        n_dpid = neigh if isinstance(neigh, str) \
            else neigh.dpid if isinstance(neigh, NetworkSwitch) \
            else None 

        if n_dpid is None:
            raise TypeError("neighid may only be str to identify the dpid, " +
                            "or the NetworkSwitch itself")

        (k, (n, swport)) = self.neighbors.pop(n_dpid)
        return n

    def addRoute(self, mac, )


class vNetAuthenticator:

    users = []
    hosts = []

    def bindUserToHost(self, user, mac):
        for h in hosts:
            if h.macAddr == mac:
                h.user = user

        raise HostNotFoundError(mac)

    def authenticate(self, username, password, mac):
        for u in self.users:
            if u.username == username
                if u.password == password:

                    try:
                        self.bindUserToHost(u, mac)

                    except HostNotFoundError as e:
                        return (False, e)

                    return (True, map(lambda n: n.vNetID, u.authroizedNetworks))

                else:
                    return (False, "Invalid password")

        return (False, "Invalid username")



class configParser:
    '''
    config = {
        'PhysicalNetwork': {
            'ipconf': ['xxx.xxx.xxx.xxx', 'yy'],
            'hosts': [ { 'mac': 'aa:aa:aa:aa:aa:aa', 'ip': '...', 'user': None, 'accessLink': ['dpid', port], 'virtualHosts': None }, ... ],
            'switches': [ { 'dpid': '...', 'neighbors': [ ... ] } ]
        },

        'VirtualNetworks': [
            { 
                'ipconf': { 'prefix': '...', 'cidr': 'yy' },
                'vNetID': '...',
                'vlan': '...',
                'hosts': []
            }
        ]
    }
    '''

    @staticmethod
    def parseIpConfig((prefix, cidr)):
        return IpConfiguration(prefix, cidr)

    @staticmethod
    def parseNetworkSwitch(sw):
        return NetworkSwitch(sw['dpid'], sw['neighbors'])


    @staticmethod
    def parseAccessLink((dpid, swport), switches):
        return AccessLink(filter(lambda sw: True if sw.dpid == dpid else False, switches)[0], swport)

    @staticmethod
    def parseHost(host):
        return PhysicalNetworkHost(host['mac'], host['ip'], )

    @staticmethod
    def parsePhysicalNetwork(physnet):
        ipconf = parseIpConfig(tuple(physnet['ipconf']))


    @staticmethod
    def initializeConfig(config):

        return None

class vNetManager:


    def __init__(self, config):
        self.physicalnetwork = PhysicalNetwork(config['PhysicalNetwork']
        self.virtualnetworks = {}
        return

    def addUserToVirtualNetwork(self, vnetid, userid, mac):

        vnet = self.virtualnetworks[vnetid]
        vhost = VirtualNetworkHost(userid)
        (sw, swport) = getAccessLink(mac)

        vnet.addHost(vhost)
        sw.addflow(swport, vhost.mac, vnet)

        return None


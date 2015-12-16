from novaclient import base
from novaclient.i18n import _
from novaclient.openstack.common import cliutils
from novaclient import utils


class Volume(base.Resource):
    """
    A volume is an extra block level storage to the OpenStack instances.
    """
    NAME_ATTR = 'display_name'

    def __repr__(self):
        return "<Volume: %s>" % self.id


class Host(base.Resource):
    def __repr__(self):
        return "<Host: %s>" % self.host


class DisasterRecoveryManager(base.Manager):
    resource_class = base.Resource

    def protect_vm(self, server):
        """
        Protect an instance

        :param server: The instance ID to protect.
        """
        resource_class = base.Resource

        action = 'drProtectVM'
        body = {action: None}
        url = '/servers/%s/action' % base.getid(server)
        return self.api.client.post(url, body=body)



    def protect_volume(self, volume):
        """
        Protect a volume

        :param server: The volume ID to protect.
        """
        resource_class = Volume

        action = 'drProtectVolume'
        body = {action: None}
        url = '/servers/%s/action' % base.getid(volume)
        return self.api.client.post(url, body=body)


    def recover(self, datacenter):
        """
        Recover a datancenter

        :param datacenter: The datacenter to recover.
        """
        resource_class = Host

        action = 'drRecover'
        body = {action: None}
        url= '/servers/%s/action' % datacenter
        return self.api.client.post(url, body=body)


@cliutils.arg(
    'server', metavar='<server>',
    help=_('ID of the VM to protect.'))
def do_protect_vm(cs, args):
    """Protect a VM."""
    server = utils.find_resource(cs.servers, args.server)
    cs.disaster_recovery.protect_vm(server)
    print "OK"


@cliutils.arg(
    'volume', metavar='<volume>',
    help=_('ID of the Volume to protect.'))
def do_protect_volume(cs, args):
    """Protect a Volume."""
    cs.disaster_recovery.protect_volume(args.volume)
    print "OK"


@cliutils.arg(
    'datacenter', metavar='<datacenter>', default='orbit1.ds.cs.umu.se',
     nargs='?', help=_('datacenter host name to recover.'))
def do_recover(cs, args):
    """Recover a Datacenter."""
    cs.disaster_recovery.recover(args.datacenter)
    print "OK"

manager_class = DisasterRecoveryManager
name = 'disaster_recovery'



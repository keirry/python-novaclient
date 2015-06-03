# Copyright (c) 2014 Umea University
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from novaclient import base
from novaclient.i18n import _
from novaclient.openstack.common import cliutils
from novaclient import utils


class FaultToleranceManager(base.Manager):
    resource_class = base.Resource

    def failover(self, server):
        url = '/servers/%s/action' % base.getid(server)
        return self.api.client.post(url, body={'failover': None})

@cliutils.arg(
    'server',
    metavar='<server>',
    help=_('Name or UUID of the failed server.'))
def do_failover(cs, args):
    server = utils.find_resource(cs.servers, args.server)
    cs.fault_tolerance.failover(server)

manager_class = FaultToleranceManager
name = 'fault_tolerance'
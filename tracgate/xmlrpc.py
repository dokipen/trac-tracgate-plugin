from trac.core import *
from trac.perm import IPermissionRequestor

from tracrpc.api import IXMLRPCHandler

class TracGateRPC(Component):
    """Interface for the tracgate lamson email application."""

    implements(IXMLRPCHandler)
    implements(IPermissionRequestor)

    # IPermissionRequestor methods
    def get_permission_actions(self):
        yield 'TRAC_GATE'

    # IXMLRPCHandler methods
    def xmlrpc_namespace(self):
        return 'tracgate'

    def xmlrpc_methods(self):
        yield ('TRAC_GATE', ((int, str, dict, str),), self.recieve)

    def recieve(self, req, body, headers, resource_uid):
        self.log.debug('body: %s'%body)
        self.log.debug('headers: %s'%headers)
        if resource_uid:
            self.log.debug('resource_uid: %s'%resource_uid)
        return 1

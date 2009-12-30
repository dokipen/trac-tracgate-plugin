from trac.core import *
from trac.perm import IPermissionRequestor
from trac.ticket.model import Ticket

from tracgate.api import ITracGateEmailHandler
from tracrpc.api import IXMLRPCHandler
from announcer.util.mail import uid_decode

class TracGateRPC(Component):
    """Interface for the tracgate lamson email application."""

    implements(IXMLRPCHandler)
    implements(IPermissionRequestor)

    handlers = ExtensionPoint(ITracGateEmailHandler)

    # IPermissionRequestor methods
    def get_permission_actions(self):
        yield 'TRAC_GATE'

    # IXMLRPCHandler methods
    def xmlrpc_namespace(self):
        return 'tracgate'

    def xmlrpc_methods(self):
        yield ('TRAC_GATE', ((int, str, dict, str),), self.recieve)

    def recieve(self, req, body, headers, resource_uid):
        if resource_uid:
            _, realm, id = uid_decode(resource_uid.upper())
            return self.handle_reply(req, realm, id, body, headers)
        return self.handle_new(req, body, headers)

    def handle_new(self, req, body, headers):
        for handler in self.handlers:
            handler.handle_new(req, body, headers)

    def handle_reply(self, req, realm, id , body, headers):
        for handler in self.handlers:
            handler.handly_reply(req, realm, id, body, headers)

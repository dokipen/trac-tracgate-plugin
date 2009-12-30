import re

from email.utils import getaddresses

from trac.core import *
from trac.ticket.model import Ticket

from tracgate.api import ITracGateEmailHandler
from tracgate.util import find_sid_by_email

TICKET_ATTR_RE = re.compile("^\s*@([^\s]+)\s+(.*)$")

class TracGateTicketEmailHandler(Component):
    """
    Something about something
    """

    implements(ITracGateEmailHandler)

    def handle_new(self, req, body, headers):
        """
        Create a new ticket
        """
        ticket = Ticket(self.env)
        ticket['summary'] = headers.get('Subject', '(No subject)')
        self.log.debug("desc: %s"%(self._strip_fields(body)))
        ticket['description'] = self._strip_fields(body)
        ticket['reporter'] = find_sid_by_email(self.env, headers.get('From'))
        ticket['cc'] = ', '.join(
            map(
                lambda i: find_sid_by_email(i[1]), 
                getaddresses(headers.get('Cc', ''))
            )
        )
        for k, v in self._find_fields(body):
            ticket[k] = v
        ticket.insert()
        return 1

    def handle_reply(self, req, realm, id, body, headers):
        """
        Add a comment to a ticket
        """
        if realm == 'ticket':
            ticket = Ticket(self.env, id)
            ticket.save_changes(headers['From'], body)
            return 1
        return 0

    def _strip_fields(self, body):
        out = []
        for line in body.split("\n"):
            m = TICKET_ATTR_RE.match(line)
            if not m:
                out.append(line)
        return "\n".join(out)

    def _find_fields(self, body):
        for line in body.split("\n"):
            m = TICKET_ATTR_RE.match(line)
            if m:
                yield m.groups()

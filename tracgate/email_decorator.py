import re
from email.utils import parseaddr, formataddr

from trac.core import *
from announcer.distributors.mail import IAnnouncementEmailDecorator
from announcer.util.mail import uid_encode, next_decorator

ADDR_REGEX = re.compile('(.*)@([^@]+)$')

class ReplyToTicketEmailDecorator(Component):

    implements(IAnnouncementEmailDecorator)

    def decorate_message(self, event, message, decorates=None):
        """
        Added headers to the outgoing email to track it's relationship
        with a ticket.  Reply-To will encode a UID as a email parameter
        so replies to the ticket announcement can be appended to the ticket.
        References, In-Reply-To and Message-ID are just so email clients can
        make sense of the threads.

        This algorithm seems pretty generic, so maybe we can make the realm
        configurable.  Any object with and id or name should work.  The 
        Reply-To header only makes sense for things that can be appended to
        through email.  Two examples are tickets and blog comments.
        """
        if event.realm == 'ticket':
            name, email_addr = parseaddr(message['Reply-To'])
            uid = uid_encode(self.env.abs_href(), event.realm, event.target)

            m = ADDR_REGEX.match(email_addr)
            new_email_addr = '%s+%s@%s'%(m.group(1), uid, m.group(2))
            new_addr = formataddr((name, new_email_addr))
            set_header(message, 'Reply-To', new_email_addr)

        return next_decorator(event, message, decorates)


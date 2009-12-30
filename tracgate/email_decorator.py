import re
from email.utils import parseaddr, formataddr

from trac.core import *
from trac.config import ListOption
from announcer.distributors.mail import IAnnouncementEmailDecorator
from announcer.util.mail import uid_encode, next_decorator, set_header

ADDR_REGEX = re.compile('(.*)@([^@]+)$')

class ReplyToEmailDecorator(Component):
    """
    Add a Reply-To header to outgoing email so we can associate replies with 
    the realm and id of the target object.
    """

    implements(IAnnouncementEmailDecorator)

    reply_to_realms = ListOption('tracgate', 'reply_to_realms', ['ticket'],
            "The realms that should include a special Reply-To header.")

    def decorate_message(self, event, message, decorates=None):
        """
        Added headers to the outgoing email to track it's relationship
        with a resource.  Reply-To will encode a UID as a email parameter
        so replies to the resource announcement can be handled by an 
        ITracGateEmailHandler.  
        """
        if event.realm in self.reply_to_realms:
            name, email_addr = parseaddr(str(message['Reply-To']))
            uid = uid_encode(self.env.abs_href(), event.realm, event.target)

            m = ADDR_REGEX.match(email_addr)
            new_email_addr = '%s+%s@%s'%(m.group(1), uid, m.group(2))
            new_addr = formataddr((name, new_email_addr))
            set_header(message, 'Reply-To', new_email_addr)

        return next_decorator(event, message, decorates)


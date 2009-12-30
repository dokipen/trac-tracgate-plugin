from trac.core import *

class ITracGateEmailHandler(Interface):
    """
    Handle emails for Trac.
    """
    def handle_new(req, body, headers):
        """
        Handle emails that aren't replies.
        """

    def handle_reply(req, realm, id, body, headers):
        """
        Handle replies to trac emails.  These include realm and id where id
        is some unique identifier in the realm.  For example, a wiki id is the
        wiki name.  In order to recieve replies, the ReplyToEmailDecorator 
        will have to be configured for the realm of you choice using the 
        reply_to_realms ListOption.
        """

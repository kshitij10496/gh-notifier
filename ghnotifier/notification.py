import subprocess

from settings import NOTIFIER

class Notification(object):
    """ Base class for all notifications.
    Every notification is of the form: "<protagonist> <context> <target>"

    Example
    =======
    In []: from ghnotifier.notification import Notification
    In []: a = Notification("kshitij10496 followed you")
    In []: print(a)
    kshitij10496 followed you
    In []: print(a.target)
    you
    In []: print(a.context)
    follow
    In []: print(a.protagonist)
    kshitij10496

    """
    def __init__(self, message):
        """
        Parameters
        ==========
        message: str
            The notification message

        """
        self.title = 'GitHub Notification'
        self.message = message
        self.target = message.split()[-1]
        self.protagonist = message.split()[:-2]
        self.context = message.split()[-2][:-2]

    @classmethod
    def generate_message(cls, target, protagonist, context):
        """
        Parameters
        ==========
        target: str
            The target user for the notification

        protagonist: str
            The protagonist of the notification

        context: str
            The context of the notification
        
        """
        message = "{} {}ed {}".format(protagonist, context, target)
        return cls(message)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.message)

    def __str__(self):
        return self.message

    def notify(self):
        """ Notifies the logged in user with an update message using the notifer application based on the Operating System.

        For MacOS : terminal-notifier
            Linux : notify-send

        """
        if NOTIFIER == "terminal-notifier"
            subprocess.run([notifier, "-title", self.title, "-message",
                                self.message, "-timeout", "10"])

        elif NOTIFIER == 'notify-send':
            subprocess.run([notifier, self.title, self.message])

        else:
            return -1

        return 1
    ## TODO: Log the notifications

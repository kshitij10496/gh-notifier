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
        self.message = message
        self.target = message.split()[-1]
        self.protagonist = message.split()[0]
        self.context = message.split()[-2][:-2]

    @classmethod
    def generate_message(cls, target, protagonist, context):
        message = "{} {}ed {}".format(protagonist, context, target)
        return cls(message)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.message)

    def __str__(self):
        return self.message

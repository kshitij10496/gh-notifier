import sys
import subprocess


def generate_message(protagonist, context, status):
    if status == 1:
        return "{} {}ed {}".format(protagonist, *context)
    elif status == 0:
        return "{} users {}ed {}".format(protagonist, *context)
    elif status == -1:
        return "{} users un{}ed {}".format(protagonist, *context)
    else:
        print("Enter valid status code for generating message")


def notify(message):
    """ Notifies the logged in user with an update message using the notifer application based on the Operating System.

    For MacOS : terminal-notifier
        Linux : notify-send

    """
    title = "GitHub Notification"
    platform = sys.platform
    if platform == 'darwin':
        # test if terminal-notifier is present on the system or not
        status = subprocess.run(["which", "terminal-notifier"]).returncode
        if status == 0:
            notifier = "terminal-notifier"
            subprocess.run([notifier, "-title", "GitHub Notification", "-message",
                            message, "-timeout", "10"])

        else:
            print("Kindly install terminal-notifier for MacOS.")
            return -1

    elif platform == 'linux':
        notifier = "notify-send"
        subprocess.run([notifier, "GitHub Notification", message])

    # look into other cases
    else:
        print("Your system is not supported yet.")
        return -1

    return 1

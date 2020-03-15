"""
Contains all the Exceptions that are raised
"""


class FullRSVP(Exception):
    """
	Unable to RSVP to event , as no spots left !
	"""

    def __init__(self):
        self.message = 'Unable to RSVP to event , as no spots left !Waitlisting instead!'


class AuthError(Exception):
    """
    Wrong username, password provided
    """

    def __init__(self):
        self.message = 'Wrong username, password provided'


class BotError(Exception):
    """
    Login failed despite correct credentials
    Bot detection, captcha enabled by site
    """

    def __init__(self):
        self.message = "Seems like bot work has been detected !\nPlease manually log in a few " \
                       "times till the captcha is remove , then try again "

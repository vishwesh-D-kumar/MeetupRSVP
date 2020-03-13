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

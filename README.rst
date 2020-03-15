Meetup-RSVP
=====================


A Python client for AutoRSVPing into Meetup Events.
Supports Python 3

Guide
===============

Installation
------------

Assuming you have python already, install the package using ``pip``:

.. code-block:: bash

    $ pip install rsvpmeetup
    
For the dev version , clone this repo and at the root directory :

.. code-block:: bash

    $ pip install .



Required
--------------------------------------
Requires a working username password of meetup to be configured
Requires user to be member of the group to be rsvpd into



Configuration
--------------------------------------
Create a secret.json file of the format

.. code-block:: json

    {
    "email": "sample@sample.com",
    "password": "passwordhere",
    "mail_id": "sample2@sample2.com",
    "mail_password":"password2"
    }

Here :
"email","password" --> your login credentials to meetup


"mail_id","mail_password" --> login to email to use for emailing on Succesful RSVP

*Less Secure Access Needs to be activated for mail_id to be used to send emails from*
https://myaccount.google.com/lesssecureapps

and a groups.json file of the format

.. code-block:: json

    {
        "groups":
        [
            {
                "urlname": "group url name here,sample below",
                "endDate":"Date in YYY-MM-DD , till when to Search for events",
                "allow_waitlist":"whether to allow for waitlist or not",
                "event_limit":"how many events to rsvp/waitlist for",
                "guest":"How many guests to allow for"
            },

            {
                "urlname": "slow-spokes",
                "allow_waitlist":true,
                "event_limit":4,
                "endDate":"2020-12-30",
                "guest":1
            }
        ]
    }


Note : both the above files must be in the same directory
Then load the configuration with

.. code-block:: bash

    rsvpcron --config $(pwd)

or

.. code-block:: bash

    rsvpcron --config path


Running
--------------------------------------


Simply run the following command from bash

.. code-block:: bash

    rsvpcron --run


For a dry run (Lists all RSVPs/Waitlists that would happen in actual run)

.. code-block:: bash

    rsvpcron --dry-run


Additional options

.. code-block:: bash

    --mail
    Mails from configured id against 'mail_id' key in secret.json to user email address (configured against 'email' key)
    Will contain all actions taken by script

Shout-out to `@cfsmp3 <https://github.com/cfsmp3>`_ , for the ideas for mailing , dry-runnning ,and adding additional configurations!

*Note : You may need to manually login a few times on error BotError being raised , It implies that the login was not successful
And most probably captcha detection has been enabled*



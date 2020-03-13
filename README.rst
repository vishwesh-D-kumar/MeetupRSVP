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
	"password": "passwordhere"
	}

and a groups.json file of the format

.. code-block:: json

    {
    	"groups":
    	[
    		{
    			"urlname": "group url name here,sample below",
    			"endDate":"Date in YYY-MM-DD , till when to Search for events"
    		},
    
    		{
    			"urlname": "slow-spokes",
    			"endDate":"2020-03-31"
    		}
    	]
    }
        

Note : both the above files must be in the same directory
Then load the configuration with 

.. code-block:: bash

    rsvpmeetup --config $(pwd)

or 

.. code-block:: bash

    rsvpmeetup --config path
    

Running
--------------------------------------


Simply run the following command from bash 

.. code-block:: bash 

    rsvpmeetup --run 





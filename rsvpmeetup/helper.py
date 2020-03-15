"""
Helper Functions
"""
import json
import pkg_resources
import yagmail


def mail(message: str):

    """
    :param message: Message to mail
    """
    user = get_config_data('secret.json')

    sender_email = user['mail_id']
    password = user['mail_password']

    receiver = user['email']
    body = 'Hey! Here are the actions taken by the cron run by you !\n' + message

    yag = yagmail.SMTP(sender_email, password)
    yag.send(
        to=receiver,
        subject="RSVP Meetup report",
        contents=body,
    )

def get_config_path():
  DATA_PATH = pkg_resources.resource_filename('rsvpmeetup', 'path.txt')

  with open(DATA_PATH,'r') as f:
    return f.read()


def get_headers(file:str)->dict:
    """
    Helper Function to get standard headers 
    which are reuquired in requests
    """
    DATA_PATH = pkg_resources.resource_filename('rsvpmeetup','headers/')

    with open(DATA_PATH+file+'_header.json','r') as f:
        return json.loads(f.read())


def get_config_data(file: str) -> dict:



    try:
        with open(get_config_path()+'/' + file, 'r') as f:
            data = json.loads(f.read())
            return data

    except FileNotFoundError as e:
        print("--" + file + " file not created--!")
        raise e  # Raising error for the stackTrace to debug later


def getToken(r:str)->str:
  tokenPos=r.find("token")
  valuePos=(r[tokenPos:]).find('value="')+tokenPos
  valueEnd=(r[valuePos+7:]).find('"')+valuePos+7
  return r[valuePos+7:valueEnd]



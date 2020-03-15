from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
setup(name='rsvpmeetup',
      version='0.4',
      long_description=readme(),
      description='A Module to Automatically rsvp yes to events in configured events for meetup.com',
      url='https://github.com/vishwesh-D-kumar/MeetupRSVP',
      author='Vishwesh Kumar',
      author_email='vishwesh18119@iiitd.ac.in',
      license='MIT',
      packages=['rsvpmeetup'],
      install_requires=[
          'requests',
            'yagmail',
      ],
      python_requires=">=3.3",
      scripts=['rsvpcron'],
      include_package_data=True,
      zip_safe=False)
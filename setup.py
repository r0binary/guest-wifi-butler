from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

tests_require = [
    'pytest',
    'mock'
]

setup(name='guest_wifi_butler',
      version='0.2.1',
      description='A Python tool to turn a Raspberry Pi with WiFi adapter and touch screen into a convenient access point for guests',
      url='http://github.com/r0binary/guest-wifi-butler',
      author='r0binary',
      author_email='r0binary@posteo.net',
      license='MIT',
      packages=find_packages(),
      install_requires=requirements,
      setup_requires=["pytest-runner"],
      tests_require=tests_require,
      scripts=['guest_wifi_butler/butler'],
      include_package_data=True,
      zip_safe=True)

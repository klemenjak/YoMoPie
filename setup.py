from setuptools import setup

try:
    from pypandoc import convert_file
    long_description = convert_file('README.md', 'md')

except ImportError:
    long_description = """
        The YoMo project aims to empower people using low-cost open-hardware energy monitor.
		With YoMoPie, we provide a user-oriented energy monitor based on the Raspberry Pi platform that aims to enable intelligent energy services in households.
		More information at: https://github.com/klemenjak/YoMoPie
"""

setup(name='YoMoPie',
      description='YoMoPie Library',
      long_description=long_description,
      version='0.1',
      url='https://github.com/klemenjak/YoMoPie',
      author='S. Jost',
      author_email='stefan.jost@aau.at',
      license='Apache2',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3'
      ],
      packages=['YoMoPie'],
      install_requires=[
          'spidev',
		  'RPi.GPIO'
      ])
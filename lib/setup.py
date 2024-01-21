from setuptools import setup, Distribution
import os
import re

setup(
        packages=['pyadms',],
        entry_points = {
            'console_scripts' : [
                'nstart = pyadms.nstart:run',
                'admsJSON = pyadms.admsJSON:run',
            ],
        },
    )

from setuptools import setup, dist
import os
import re

#https://stackoverflow.com/questions/35112511/pip-setup-py-bdist-wheel-no-longer-builds-forced-non-pure-wheels/36886459#36886459
#https://stackoverflow.com/questions/24071491/how-can-i-make-a-python-wheel-from-an-existing-native-library/24793171#24793171
#https://github.com/google/or-tools/issues/616
class BinaryDistribution(dist.Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(self):
        return True
    def is_pure(self):
        raise RuntimeError("HERE")
        return False

setup(
        packages=['pyadms',],
        entry_points = {
            'console_scripts' : [
                'nstart = pyadms.nstart:run',
                'admsJSON = pyadms.admsJSON:run',
            ],
        },
        package_dir = {
            '' : 'lib',
        },
        package_data={
            'pyadms' : ['./admsJSON',],
        },
        distclass=BinaryDistribution,
        #include_package_data=True,
    )

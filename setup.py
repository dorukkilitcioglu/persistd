from setuptools import setup, find_packages


setup(
    name='persistd',
    version='1.2.0',
    author='Doruk Kilitcioglu',
    author_email='doruk.kilitcioglu@gmail.com',
    install_requires=["requests"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'persist=persistd.persist:main_cmd',
        ],
    },
    include_package_data=True,
    url='https://github.com/dorukkilitcioglu/persistd',
    license='GPLv3',
    long_description=open('README.md').read(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
)

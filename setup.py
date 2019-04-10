from setuptools import setup, find_packages

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='persistd',
    version='1.2.1',
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
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
)

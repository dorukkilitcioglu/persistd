# https://packaging.python.org/guides/distributing-packages-using-setuptools/#uploading-your-project-to-pypi

python setup.py sdist

python setup.py bdist_wheel

twine upload --skip-existing dist/*
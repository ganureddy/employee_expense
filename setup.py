from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in employee_expense/__init__.py
from employee_expense import __version__ as version

setup(
	name="employee_expense",
	version=version,
	description="Employee Expense",
	author="Kareem",
	author_email="kareem@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

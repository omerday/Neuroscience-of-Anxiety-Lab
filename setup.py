from setuptools import setup, find_packages

def read_requires():
    with open("Assignments/Doors/requirements.txt", "rt") as req_f:
        requirements = []
        for req in req_f.readlines():
            requirements.append(req)
    return requirements

setup(
    name='Doors-Task',
    version='1.0.0',
    packages=find_packages(),
    url='',
    license='',
    author='odayan',
    author_email='',
    description='',
    python_requires='>=3.8.6',
    install_requires=read_requires()
)

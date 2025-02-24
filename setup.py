from setuptools import setup, find_packages

setup(
    name='PyNetQIR',
    version='0.1.0',
    packages=find_packages(),
    author='F. Javier Cardama',
    author_email='javier.cardama@usc.es',
    description='NetQIR SDK for Python',
    url='https://github.com/NetQIR/PyNetQIR',  # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
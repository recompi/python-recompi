from setuptools import setup, find_packages

# Read requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line and not line.startswith('#')]


setup(
    name='recompi',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['requests'],
    author='RecomPI',
    author_email='tech@recompi.com',
    description='A Python wrapper for the Recompi API',
    install_requires=parse_requirements('requirements.txt'),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/recompi/recompi',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7',
)

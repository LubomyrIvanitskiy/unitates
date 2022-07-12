from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='unitates',
    version='1.0.13',
    packages=['tests', 'units', 'units.constants'],
    url='',
    license='MIT License',
    author='liubomyr.ivanitskyi',
    author_email='lubomyr.ivanitskiy@gmail.com',
    description='Python library for working with custom and predefined number measurement units',
    long_description=readme(),
    long_description_content_type="text/markdown"
)

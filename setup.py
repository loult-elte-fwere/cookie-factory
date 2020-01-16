from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name='cookie-factory',
    version='0.1',
    description="A small package to render loult cookie properties",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hadware',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='cookies',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'])

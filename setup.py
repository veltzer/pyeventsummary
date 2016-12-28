import setuptools

setuptools.setup(
    name='pyeventsummary',
    version='0.0.2',
    description='pyeventsummary is a way to aggregate and report on a host of errors and actions',
    long_description='pyeventsummary is a way to aggregate and report on a host of errors and actions',
    url='https://veltzer.github.io/pyeventsummary',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='python summary errors actions aggregate print enum',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
)

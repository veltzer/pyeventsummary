import setuptools

setuptools.setup(
    name='pyeventsummary',
    version='0.0.15',
    description='pyeventsummary is a way to aggregate and report on a host of errors and actions',
    long_description='pyeventsummary is a way to aggregate and report on a host of errors and actions',
    url='https://veltzer.github.io/pyeventsummary',
    download_url='https://github.com/veltzer/pyeventsummary',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='python summary errors actions aggregate print enum',
    packages=setuptools.find_packages(),
)

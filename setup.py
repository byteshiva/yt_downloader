from setuptools import setup, find_packages

setup(
    name='youtube-downloader',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'pytube',
        'youtube_dl'
    ],
)

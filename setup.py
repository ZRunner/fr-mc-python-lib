from setuptools import setup

setup(
    name="frmc_lib",
    version = "1.0.0a",
    description = 'A Python 3 library that allows you to retrieve Minecraft game information from the fr-minecraft.net website',
    author = 'ZRunner',
    author_email = 'z.runner.mc@gmail.com',
    url = 'https://github.com/ZRunner/fr-mc-python-lib.git',
    py_modules=['frmc_lib'],
    install_requires=[
        'requests',
        'regex'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)

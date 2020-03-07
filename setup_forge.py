import setuptools

setuptools.setup(
    name = 'Uno Game-Forge',
    version = '1.1b5',
    url = 'https://github.com/gaming32/uno',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = 'Modding for Uno Game',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    install_requires = [
        'Uno-Game>=1.1b5',
    ],
    py_modules = [
        'uno_forge',
        'unoforge',
    ],
    scripts = [
        'uno_forge.py',
    ],
)
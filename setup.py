import setuptools

setuptools.setup(
    name = 'Uno Game',
    version = '1.1b8',
    url = 'https://github.com/gaming32/uno',
    author = 'Gaming32',
    author_email = 'gaming32i64@gmail.com',
    license = 'License :: OSI Approved :: MIT License',
    description = 'A recreation of the Uno card game',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    install_requires = [
        'numpy',
        'Network-Script>=1.0.5',
    ],
    packages = [
        'uno',
        'uno._network',
    ],
)
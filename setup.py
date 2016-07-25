from distutils.core import setup

setup(
    name='asyncio-map-pool',
    author='Evgeniy Malov',
    author_email='evgeniiml@gmail.com',
    version='0.1',
    packages=['.',],
    requires = ['python (>= 3.5)',],
    license='MIT',
    description="class-less map pool for asyncio coroutines",
    keywords = ["asyncio","map","imap","pool"]
)
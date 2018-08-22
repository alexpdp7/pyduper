from setuptools import setup, find_packages

setup(name='pyduper',
      py_modules=['pyduper'],
      extras_require={
        'dev': ['ipython', 'ipdb',],
      },
      python_requires='>=3',
)
      
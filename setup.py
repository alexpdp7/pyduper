from setuptools import setup, find_packages

setup(name='pyduper',
      packages=find_packages(),
      extras_require={
        'dev': ['ipython', 'ipdb',],
      },
      python_requires='>=3',
)
      
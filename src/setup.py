from setuptools import setup

setup(name='dublin_bikes',
      version='0.1',
      description='Program to test LED board',
      author = 'Pamela Kelly, Emma Byrne, Katherine Campbell',
      url='https://github.com/PamelaKelly/Assignment4-P-E-K',
      license = 'GNU',
      packages = ['dublin_bikes'],
      entry_points = {
          'console_scripts': ['scraper=dublin_bikes.scraper:scraper']
          }
      )

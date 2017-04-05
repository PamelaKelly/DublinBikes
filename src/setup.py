from setuptools import setup

setup(name='dublin_bikes',
      version='0.1',
      description='Dublin Bikes Web Application Project',
      author = 'Pamela Kelly, Emma Byrne, Katherine Campbell',
      url='https://github.com/PamelaKelly/Assignment4-P-E-K',
      license = 'GNU',
      packages = ['scraper'],
      entry_points = {
          'console_scripts': [
              'scraper=scraper.scraper:run_scraper',
              'files_to_db=scraper.scraper:multiple_files_to_db'
            ]
          }
      )

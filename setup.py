from setuptools import setup
import pathlib

# getting the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(name="invest_tracker",
      version="0.1",
      description="Helps to track and manage investments",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/leofmr/invest_tracker",
      author="Leonardo Rocha",
      author_email="leonardo@moutinho.com.br",
      install_requires=['pandas', 'investpy'],
      packages=["invest_tracker"],
      zip_safe=False)
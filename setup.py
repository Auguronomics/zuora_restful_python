from setuptools import setup
setup(
  name = 'zuora_restful_python',
  packages = ['zuora_restful_python'], 
  version = '0.32',
  description = 'zuora REST API wrapper',
  author = 'Bo Laurent',
  author_email = 'bo@bolaurent.com',
  url = 'https://github.com/auguronomics/zuora_restful_python', 
  keywords = ['zuora', 'rest', 'api'], 
  classifiers = [
    'Programming Language :: Python :: 3'
  ],
  install_requires=[
        "requests"
    ]
)

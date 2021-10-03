from setuptools import setup

setup(name='stavroslib',
      version='0.21',
      description='My common libraries',
      url='https://github.com/spitoglou/stavros-lib',
      author='Stavros Pitoglou',
      author_email='s.pitoglou@csl.gr',
      license='MIT',
      packages=['stavroslib'],
      #   test_suite='nose.collector',
      tests_require=['pytest'],
      install_requires=[
          'requests',
          'loguru',
          'plyer',
          'reportlab',
          'PyYAML'
          #   'scikit-learn',
          #   'numpy',
          #   'matplotlib'
      ],
      zip_safe=False)

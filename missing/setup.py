from setuptools import setup, find_packages

setup(name="missing",
      version="0.0.2",
      packages=find_packages(),
      license='MIT',
      entry_points={
          'console_scripts': [
              'du_by_ext=du_by_ext:main',
              'git_set_user=git_set_user:main',
          ]
      }
)


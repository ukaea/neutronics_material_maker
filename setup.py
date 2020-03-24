import setuptools

<<<<<<< HEAD
from setuptools import setup

#with open('requirements.txt') as test_reqs_txt:
#    requirements = [line for line in test_reqs_txt]


setup(name='neutronics_material_maker',
      version='0.1233.1',
      summary='Package for making material cards for neutronic codes such as Serpent',
      description='Create isotopes, elements, materials, chemical compounds and homogenised mixtures for use in neutronics codes',
      url='https://github.com/ukaea/neutronics_material_maker',
      author='Jonathan Shimwell',
      author_email='jonathan.shimwell@ukaea.uk',
      license='Apache 2.0',
      packages=['neutronics_material_maker'],
      # test_suite='tests.module_tests',
      test_suite='tests.testsuite',
      zip_safe=False,
      include_package_data=True,
      package_data={'':['requirements.txt', 'README.md', 'LICENSE','nuclear_data.csv']},
      #install_requires=requirements,
      #setup_requires=['pytest-runner'],
      tests_require=['pytest']
      )
=======
# with open("README.md", "r") as fh:
#     long_description = fh.read()
>>>>>>> git_actions_test_branch

setuptools.setup(
    name="neutronics_material_maker",
    version="0.1235.21",
    summary='Package for making material cards for OpenMC',
    author="Jonathan Shimwell",
    author_email="jonathan.shimwell@ukaea.uk",
    description="A tool for making neutronics material cards for use in OpenMC",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ukaea/neutronics_material_maker",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'':['requirements.txt', 'README.md', 'LICENSE']},
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    #     "Operating System :: OS Independent",
    # ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest-cov',
    ],
    install_requires = [
        'coolprop',
	#'openmc' when pip install is available
    ]
)

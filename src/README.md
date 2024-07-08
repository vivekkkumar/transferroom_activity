**Introduction** 

I bootstrapped this project by giving a structure similar to maven project(not exactly similar) 
but seperating src and tests if the project evolves the tests would have same directory structure as the source. 

**Requirements**

To run these scripts locally we need to have these below requirements.
1. Python 3.10.0 (I just chose it since I used this version recently)
2. I did that by installing, pyenv, pyenv-virtualenv and then
commands: 

`%pyenv install 3.10.0`

`%pyenv virtualenv 3.10 viooh_activity`

3. Run the below commands,

`echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc`

`echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
`

`echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
`

`echo 'eval "$(pyenv init -)"' >> ~/.zshrc
`

`echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
`

``source ~/.zshrc`
``

`%pyenv activate viooh_activity
`

``%pip install -r requirements.txt`
``

or on bash
4. To run tests locally install **"Make"** by brew install make if on Mac or apt-get install -y make
5. And then add the python path : `export PYTHONPATH="your_directory/viooh_activity:$PYTHONPATH"`
6. To run the tests run make test or pytest tests/
7. To run the main program run `spark-submit src/app/session_creator.py`

**Explanation**

1. The project has an app folder which is the main entry point of the script
2. There is a models foldr, where all the schemas are placed (It is always better to provide schemas explicitely)
3. The transformations folder has implementation of all the methods the main script calls, I have separated and parameterised the modules so we can test them easily.
4. resources folder has files or might contain configs in future if needed for various environments to be used in the script and also has the output folder for this activity.
5. There is a Makefile which can be used to run commands in CI to install dependancies and make a checking for the test to pass before deploying
6. I did not create a deployment mechanism, but the commands I provide below can be added to a bash script or in a Dockerfile to be deployed.
7. I have used Pyspark as the engine so that even if there is change in size of data or running engine (either EMR or databricks etc) we can deploy the script and run by tweaking few parameters like partition and different sources and sinks.

**Things not considered**
1. The CD part is not considered since I felt currently all these commands can be run locally for testting
2. If the project evolves we can create a Dockerfile with all the commands I mentioned above and can be deployed as an docker image for EMR or databricks engine.
3. Tests may look very simple as they don't test all the functionality but I created them to show it works in this project.
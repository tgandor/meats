call conda create -y -n test_environment python=3.6
echo create done
call activate test_environment
echo activate done
pip install pylint==1.8
echo pip installed
pip list
pip install "pylint>=1.8"
pip list
call deactivate
call conda env remove -y -n test_environment

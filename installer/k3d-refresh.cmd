@echo off

if not defined CONDA_DEFAULT_ENV if not defined VIRTUAL_ENV (
    echo Not in VirtualEnv or Conda Env, exiting
    exit /b 1
)

pushd js 2> NUL
if ERRORLEVEL 1 (
    echo "Probably in the wrong directory: no js/ subdir, exiting"
    exit /b 1
)

echo on

call grunt build
popd

pip install -e .

jupyter nbextension install --py --sys-prefix k3d
jupyter nbextension enable --py --sys-prefix k3d
jupyter nbextension list

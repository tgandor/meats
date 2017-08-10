if not defined CONDA_DEFAULT_ENV if not defined VIRTUAL_ENV (
    echo Not in VirtualEnv or Conda Env, exiting
    exit /b
)

pip install -e .

jupyter nbextension enable --py widgetsnbextension --sys-prefix
jupyter nbextension install --py --sys-prefix k3d
jupyter nbextension enable --py --sys-prefix k3d
jupyter nbextension list

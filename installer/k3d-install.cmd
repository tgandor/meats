pip install -e .

if not defined VIRTUAL_ENV (
    echo Not in VirtualEnv, exiting
    exit /b
)

jupyter nbextension enable --py widgetsnbextension --sys-prefix
jupyter nbextension install --py --sys-prefix k3d
jupyter nbextension enable --py --sys-prefix k3d
jupyter nbextension list

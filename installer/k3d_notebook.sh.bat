:: bringing back the old toy; 'data_files' works no more? &>/dev/null
:: run in K3D-jupyter directory, BTW

pip install -e .
jupyter nbextension install --user --py k3d
jupyter nbextension enable --user --py k3d


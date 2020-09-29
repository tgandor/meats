echo User installation
echo pip install jupyter_contrib_nbextensions --user
echo jupyter nbextensions_configurator enable --user
echo ------
echo Alternative: https://tljh.jupyter.org/en/latest/howto/admin/enable-extensions.html
echo ------
echo pip install jupyter_contrib_nbextensions
echo Then maybe:
echo jupyter contrib nbextension install --sys-prefix
echo ------
echo And then, e.g.:
echo jupyter nbextension enable scratchpad/main --sys-prefix
echo jupyter nbextension enable toc2/main

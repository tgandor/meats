@echo off

for /D %%f in (*) do (
    if exist %%f\.git (
        pushd %%f
        cd
        git pull --ff-only
        echo ----------------------------------
        popd
    )
)

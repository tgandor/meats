@echo off

if [%1]==[] (
    for /D %%f in (*) do (
        if exist %%f\.git (
            pushd %%f
            cd
            git pull --ff-only
            echo ----------------------------------
            popd
        )
    )
    exit /b
)

for %%d in (%*) do (
    if exist %%d\.git (
            pushd %%d
            cd
            git pull --ff-only
            echo ----------------------------------
            popd
    )
)

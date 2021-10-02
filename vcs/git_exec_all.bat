@echo off

for /D %%f in (*) do (
    if exist %%f\.git (
        pushd %%f
        cd
        call %*
        echo ----------------------------------
        popd
    )
)
exit /b

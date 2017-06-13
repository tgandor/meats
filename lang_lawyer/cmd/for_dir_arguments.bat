@echo off

echo Arguments: %*

echo Directories: (this doesn't work: /D switch does nothing here)
for /D %%p in (%*) do (
    echo Dir: %%p
)

echo All:
for %%p in (%*) do (
    echo Argument: %%p
    if exist %%p\ echo   /Probably a directory/
)


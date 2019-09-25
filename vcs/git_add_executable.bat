@echo off

:: thanks to: https://stackoverflow.com/a/21694391/1338797

git add %*
git update-index --chmod=+x %*
git status

:: this prints too many (i.e. all) files...
:: git ls-files --stage

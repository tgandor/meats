@rem Check CL in path without output 
:: @setlocal
@where cl >nul 2>nul && echo present || echo missing, adding && call "%VS140COMNTOOLS%vsvars32.bat"
@where cl >nul 2>nul && cl || echo VS 2015 still not found

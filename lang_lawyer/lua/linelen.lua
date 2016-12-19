#!/usr/bin/env luajit

for line in function() return io.read() end do
   print(#line, line)
end


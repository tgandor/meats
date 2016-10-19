-- just registers globally

function dump(t)
   if type(t) == 'table' then
      io.write('{ ')
      for k, v in pairs(t) do
         dump(k)
         io.write(' -> ')
         dump(v)
         io.write(', ')
      end
      io.write('}')
   else
      io.write(tostring(t))
   end
end

function dumpln(t)
    dump(t)
    io.write('\n')
end

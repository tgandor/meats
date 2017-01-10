
num_columns = #arg < 1 and 100 or tonumber(arg[1])
stride = #arg < 2 and 5 or tonumber(arg[2])

function pad(s, n, c)
    c = c or ' '
    while #s < n do
        s = c .. s
    end
    return s
end

line, total = '', 0

while total < num_columns do
    total = total + stride
    line = line .. pad(tostring(total), stride, '.')
end

print(line)

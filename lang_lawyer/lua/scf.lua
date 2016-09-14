local function simple_copy_file(src, dst)
    local f_input = assert(io.open(src, 'rb'), 'Source file `' .. src .. '` not found')
    local f_output = assert(io.open(dst, 'wb'), 'Cannot open `' .. dst .. '` for writing')
    local data = f_input:read('*all')
    f_output:write(data)
    f_input:close()
    f_output:close()
end

return simple_copy_file


function thousands(value, sep)
	sep = sep or ','
	naive = tostring(value):reverse():gsub('(%d%d%d)', '%1'..sep):reverse()
	return (#naive % 4 == 0) and naive:sub(2, #naive) or naive
end

mul_pattern = '((%d+)%s*x%s*(%d+))'

function sub_multiplications(expr, a, b)
	return expr .. ' = ' .. thousands(tonumber(a) * tonumber (b))
end

line = io.read()
while line do
	line = line:gsub(mul_pattern, sub_multiplications)
	print(line)
	line = io.read()
end

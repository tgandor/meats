
function range(n)
	local i = -1
	return function()
		i = i + 1
		if i < n then
			return i
		end
	end
end

for i in range(tonumber(arg[1] or 10)) do
	print(i)
end

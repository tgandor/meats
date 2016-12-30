local queue = {}

function queue:push(t)
	self.last = self.last + 1
	self[self.last] = t
end

function queue:front()
	return self[self.first]
end

function queue:pop()
	self[self.first] = nil
	self.first = self.first + 1
end

function queue:iter()
	local i = self.first
	return function()
		if i <= self.last then
			i = i + 1
			return self[i-1]
		else
			return nil
		end
	end
end

function queue:has()
	return self.first <= self.last
end

function queue.new(o)
	o = o or {}
	o.first = 0
	o.last = -1
	return setmetatable(o, {__index = queue})
end

return queue

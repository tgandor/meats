-- to see the messages appearing, go to "Messages" tab,
-- if results is being displayed!

declare @last_batch as datetime;
declare @now as datetime;
-- declare @delta as varchar(30);
declare @i as Int;

set @last_batch = GETDATE();
set @now = GETDATE();
set @i = 1;

while @i < 10 begin
	waitfor delay '00:00:01';
	set @now = getdate();
	-- print with flush:
	-- set @delta = convert(varchar(30), (@now - @last_batch), 8);
	-- raiserror('%d iteration: %s', 0, 1, @i, @delta) with nowait;

	-- not needed: flushing can be done by a separate RAISERROR:
	print concat(@i, ' ', format(@now, 'HH:mm:ss'), ' ', cast(@now - @last_batch as time));
	RAISERROR(N'', 0, 1) WITH NOWAIT;

	set @i = @i + 1;
	set @last_batch = getdate();
end;

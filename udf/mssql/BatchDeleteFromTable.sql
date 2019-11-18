-- To delete many rows from a large table:
-- Edit query below,
-- which would otherwise explode your log file to gigabytes,
-- fill it up, and finaly fail and rollback...

DECLARE @Deleted_Rows INT;
DECLARE @Last_Deleted_Rows INT;

declare @last_batch as datetime;
declare @now as datetime;
declare @start as datetime;
declare @i as Int;

set @last_batch = GETDATE();
set @now = GETDATE();
set @start = GETDATE();
set @i = 1;

SET @Deleted_Rows = 0;
SET @Last_Deleted_Rows = 1;

WHILE (@Last_Deleted_Rows > 0)
  BEGIN

  -- QUERY HERE
  -- Delete some small number of rows at a time
  delete top(1000000) from users 
  where 1=1

  SET @Last_Deleted_Rows = @@ROWCOUNT;
  SET @Deleted_Rows = @Deleted_Rows + @Last_Deleted_Rows;

  set @now = getdate();
  print concat(@i, ': ', format(@now, 'HH:mm:ss'), 
    ' deleted ', @Last_Deleted_Rows, ' in ',  cast(@now - @last_batch as time),
    ', total: ', @Deleted_Rows, ' in ', cast(@now - @start as time));
  RAISERROR(N'', 0, 1) WITH NOWAIT;

  set @i = @i + 1;
  set @last_batch = getdate();
END

-- Putting this here, to not search for it every few months:
-- https://stackoverflow.com/questions/56628/how-do-you-clear-the-sql-server-transaction-log/
-- https://stackoverflow.com/a/18292136/1338797

ALTER DATABASE yourdb SET RECOVERY SIMPLE;

USE yourdb;
GO
CHECKPOINT;
GO
CHECKPOINT; -- run twice to ensure file wrap-around
GO
DBCC SHRINKFILE(yourdb_log, 1); -- unit is set in MBs
GO

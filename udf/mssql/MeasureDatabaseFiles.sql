DBCC SQLPERF(LOGSPACE);

SELECT mf.[name]
	,total_page_count * 8192 AS TotalBytes
	,allocated_extent_page_count * 8192 AS AllocatedBytes
	,100 * allocated_extent_page_count / total_page_count AS PercentAllocated
	,*
FROM sys.dm_db_file_space_usage fsu
INNER JOIN sys.master_files mf ON fsu.file_id = mf.file_id
	AND mf.database_id = fsu.database_id

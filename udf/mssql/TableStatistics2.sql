WITH TableInfo
AS (SELECT s.name AS SchemaName,
           t.name AS TableName,
           p.rows AS NumRows,
           CAST(ROUND((SUM(a.used_pages) / 128.00), 2) AS NUMERIC(36, 2)) AS Used_MB,
           CAST(ROUND((SUM(a.total_pages) - SUM(a.used_pages)) / 128.00, 2) AS NUMERIC(36, 2)) AS Unused_MB,
           CAST(ROUND((SUM(a.total_pages) / 128.00), 2) AS NUMERIC(36, 2)) AS Allocated_MB
    FROM sys.tables t
        INNER JOIN sys.indexes i
            ON t.object_id = i.object_id
        INNER JOIN sys.partitions p
            ON i.object_id = p.object_id
               AND i.index_id = p.index_id
        INNER JOIN sys.allocation_units a
            ON p.partition_id = a.container_id
        INNER JOIN sys.schemas s
            ON t.schema_id = s.schema_id
    GROUP BY t.name,
             s.name,
             p.rows)
SELECT -- TableInfo.SchemaName,
       TableInfo.TableName,
       TableInfo.NumRows,
       TableInfo.Used_MB,
       SUM(TableInfo.Used_MB) OVER (ORDER BY TableInfo.Used_MB DESC) Total_Used_MB
FROM TableInfo
-- WHERE TableInfo.SchemaName = ''
ORDER BY TableInfo.Used_MB DESC;

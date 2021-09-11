WITH
TableInfo AS (SELECT s.name AS SchemaName,
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
             p.rows),
SchemaInfo AS (SELECT TableInfo.SchemaName,
           COUNT(TableInfo.TableName) AS Num_Tables,
           SUM(TableInfo.NumRows) AS Total_Rows,
           SUM(TableInfo.Used_MB) AS Total_Used_MB
    FROM TableInfo
    GROUP BY TableInfo.SchemaName)
SELECT SchemaInfo.SchemaName,
       SchemaInfo.Num_Tables,
       SchemaInfo.Total_Rows,
       SUM(SchemaInfo.Total_Rows) OVER (ORDER BY SchemaInfo.Total_Used_MB DESC) GT_Rows,
       SchemaInfo.Total_Used_MB,
       SUM(SchemaInfo.Total_Used_MB) OVER (ORDER BY SchemaInfo.Total_Used_MB DESC) GT_MB
FROM SchemaInfo
ORDER BY SchemaInfo.Total_Used_MB DESC;

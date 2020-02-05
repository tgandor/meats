-- shows tables which have no hanging foreign keys on them
-- need to see still, if this is always enough...

-- SELECT for showing the tables which can be dropped right off the bat

select DISTINCT
    s.name + '.' + t.Name AS TableName,
    p.rows AS RowCounts
FROM
	sys.tables t
    INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
    INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
where
    p.rows = 0 and
    t.object_id not in (select referenced_object_id from sys.foreign_keys)

-- SELECT for showing empty tables which have foreign keys refering to them
-- (with the names of these keys together with the parent table)

select DISTINCT
    s.name + '.' + t.Name AS TableName,
    p.rows AS RowCounts,
	tf.name AS ReferencingTable,
    f.name AS ForeignKey
FROM
	sys.tables t
    INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
    INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
    INNER JOIN sys.foreign_keys f on f.referenced_object_id = t.object_id
	INNER JOIN sys.tables tf ON tf.object_id = f.parent_object_id
where p.rows = 0

-- PROCEDURE for generating the SQL to drop the non-foreign key tables.
-- You can run it multiple times, to have "recursive" dependencies on empty tables removed
-- before finding the newly freed direct descendants.

IF OBJECT_ID('dbo.usp_DropEmptyTables', 'P') IS NOT NULL
	DROP PROCEDURE [dbo].[usp_DropEmptyTables]
GO

CREATE PROCEDURE [dbo].[usp_DropEmptyTables]
AS
BEGIN
    DECLARE @sql NVARCHAR(max) = ''
    select
        @sql = @sql + 'drop table ['+ s.name + '].[' + t.Name + '];' + CHAR(13) + CHAR(10)
    FROM
        sys.tables t
        INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
        INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
    where
        p.rows = 0 and
        t.object_id not in (select referenced_object_id from sys.foreign_keys)
    GROUP BY s.name, t.Name -- not sure if 'distinct @sql = ...' would be possible

    if @sql = ''
        print '-- no tables to drop...'
    ELSE
        PRINT @sql

    print 'GO -- DO NOT FORGET'
    -- uncomment to do it, instead of talking:
    -- EXEC sp_executesql @sql
END
GO

EXEC usp_DropEmptyTables

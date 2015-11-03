IF OBJECT_ID('dbo.usp_ColumnReport', 'P') IS NOT NULL
	DROP PROCEDURE [dbo].[usp_ColumnReport]
GO

CREATE PROCEDURE [dbo].[usp_ColumnReport] (
	@columnName SYSNAME
	,@schema SYSNAME = 'dbo'
	,@resultTable SYSNAME = NULL
	)
AS
BEGIN
	DECLARE @sql NVARCHAR(max) = 'SELECT '''' as tableName, NULL as [value], 0 as [count], 0 as [percent] where 0=1' + CHAR(13) + CHAR(10);

	SELECT @sql = @sql 
	   + 'union all SELECT ''' + ST.[name] + ''' AS tableName, ' 
	   + @columnName + ' AS [value], COUNT(*) as [count], CAST(100.0 * COUNT(*) / (SELECT COUNT(*) FROM ' 
	   + SCHEMA_NAME(ST.schema_id) + '.' + ST.[name] + ') AS DECIMAL(18,4)) as [percent]  FROM ' 
	   + SCHEMA_NAME(ST.schema_id) + '.' + ST.[name] + ' GROUP BY ' + @columnName + CHAR(13) + CHAR(10)
	FROM sys.tables ST
	JOIN sys.columns SC ON SC.object_id = ST.object_id
	JOIN sys.schemas SS ON SS.schema_id = ST.schema_id
	WHERE SC.[name] = @columnName
		AND SS.[name] like @schema;

	SET @sql = @sql + 'ORDER BY [tableName], [value] '

	IF @resultTable IS NULL 
	   EXEC sp_executesql @sql

	IF @resultTable IS NOT NULL 
	BEGIN
	   DECLARE @dropSql NVARCHAR(MAX) = '
		  IF OBJECT_ID(''tempdb..'+@resultTable+''') IS NOT NULL
			 BEGIN
				DROP TABLE '+@resultTable+'
			 END'
	   EXEC sp_executesql @dropSql

	   DECLARE @execSql NVARCHAR(MAX) = '
		  CREATE TABLE '+@resultTable+' (
			  [tableName] SYSNAME
			  ,[value] VARCHAR(max)
			  ,[count] INT
			  ,[percent] DECIMAL(18, 4)
		  );
		  DECLARE @innerSql NVARCHAR(MAX) = ''' + REPLACE(@sql, '''', '''''') + ''';
		  INSERT INTO '+@resultTable+' 
		  EXEC sp_executesql @innerSql;
	   '
	   PRINT @execSql;
	   EXEC sp_executesql @execSql
	END
END
GO

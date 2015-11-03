IF OBJECT_ID('dbo.usp_FindColumns', 'P') IS NOT NULL
	DROP PROCEDURE [dbo].[usp_FindColumns]
GO

CREATE PROCEDURE [dbo].[usp_FindColumns] (
	@columnName SYSNAME
	,@schema SYSNAME = '%'
	)
AS
BEGIN
    SELECT SS.[name] as [schema], ST.[name] as [table], SC.[name] as [column] 
    FROM sys.all_columns SC
    JOIN sys.tables ST ON ST.object_id = SC.object_id
    JOIN sys.schemas SS ON SS.schema_id = ST.schema_id
    WHERE SC.[name] like @columnName
	   AND SS.[name] like @schema
END
GO

IF OBJECT_ID('dbo.usp_FindColumnsEx', 'P') IS NOT NULL
	DROP PROCEDURE [dbo].[usp_FindColumnsEx]
GO

CREATE PROCEDURE [dbo].[usp_FindColumnsEx] (
	@columnName SYSNAME
	,@schema SYSNAME = '%'
	,@resultTable SYSNAME = NULL
)
AS
BEGIN
    IF @resultTable IS NULL
	   EXEC [dbo].[usp_FindColumns] @columnName, @schema
    ELSE
    BEGIN
	   DECLARE @dropSql NVARCHAR(MAX) = '
		  IF OBJECT_ID(''tempdb..'+@resultTable+''') IS NOT NULL
			 BEGIN
				DROP TABLE '+@resultTable+'
			 END'
	   EXEC sp_executesql @dropSql

	   DECLARE @execSql NVARCHAR(MAX) = '
		  CREATE TABLE '+@resultTable+' (
			  [schema] SYSNAME
			  ,[table] SYSNAME
			  ,[column] SYSNAME
		  );
		  INSERT INTO '+@resultTable+' 
		  EXEC [dbo].[usp_FindColumns] ''' + @columnName + ''', ''' + @schema + ''';'
	   EXEC sp_executesql @execSql
    END
END
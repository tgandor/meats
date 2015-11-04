-- http://www.brentozar.com/blitz/foreign-key-trusted/

IF OBJECT_ID('dbo.usp_RepairUntrustedForeignKeys', 'P') IS NOT NULL
	DROP PROCEDURE [dbo].[usp_RepairUntrustedForeignKeys]
GO

CREATE PROCEDURE [dbo].[usp_RepairUntrustedForeignKeys]
AS
BEGIN
	DECLARE @sql NVARCHAR(max) = '';

	WITH BrokenKeys(tableName, keyName) AS (
			SELECT '[' + SS.[name] + '].[' + SO.[name] + ']'
				,'[' + SFK.[name] + ']'
			FROM [sys].[foreign_keys] SFK
			INNER JOIN [sys].[objects] SO ON SO.[object_id] = SFK.[parent_object_id]
			INNER JOIN [sys].[schemas] SS ON SS.[schema_id] = SO.[schema_id]
			WHERE SFK.[is_not_trusted] = 1
				AND SFK.[is_not_for_replication] = 0
			)

	SELECT @sql = @sql + 'ALTER TABLE ' + tableName + ' WITH CHECK CHECK CONSTRAINT ' + keyName + ';' + CHAR(13) + CHAR(10)
	FROM BrokenKeys;

	PRINT @sql;
	EXEC sp_executesql @sql;
END
GO

-- Based on:
-- https://stackoverflow.com/questions/44034/how-can-i-get-the-definition-body-of-a-trigger-in-sql-server

-- consider also:

-- SELECT definition
-- FROM sys.sql_modules
-- WHERE object_id = OBJECT_ID('trigger_name');

-- SELECT OBJECT_NAME(parent_obj) [table name],
--    NAME [triger name],
--    OBJECT_DEFINITION(id) body
-- FROM sysobjects
-- WHERE xtype = 'TR'
--   AND name = 'trigger_name';

-- SELECT OBJECT_DEFINITION(OBJECT_ID('trigger_name')) AS trigger_definition;

-- EXEC sp_helptext 'trigger_name';

SELECT
    DB_NAME() AS DataBaseName,
    dbo.SysObjects.ID as ObjectId,
    dbo.SysObjects.Name AS TriggerName,
    dbo.sysComments.Text AS SqlContent
FROM
    dbo.SysObjects INNER JOIN
    dbo.sysComments ON dbo.SysObjects.ID = dbo.sysComments.ID
WHERE
    dbo.SysObjects.xType = 'TR'

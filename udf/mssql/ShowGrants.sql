-- Collected from:
-- https://stackoverflow.com/questions/497317/how-can-i-view-all-grants-for-an-sql-database

-- Version 1: --

SELECT
    class_desc
  , CASE WHEN class = 0 THEN DB_NAME()
         WHEN class = 1 THEN OBJECT_NAME(major_id)
         WHEN class = 3 THEN SCHEMA_NAME(major_id) END [Securable]
  , USER_NAME(grantee_principal_id) [User]
  , permission_name
  , state_desc
FROM sys.database_permissions

-- Version 2: --

select
    class_desc
    ,USER_NAME(grantee_principal_id) as user_or_role
    ,CASE WHEN class = 0 THEN DB_NAME()
          WHEN class = 1 THEN ISNULL(SCHEMA_NAME(o.uid)+'.','')+OBJECT_NAME(major_id)
          WHEN class = 3 THEN SCHEMA_NAME(major_id) END [Securable]
    ,permission_name
    ,state_desc
    ,'revoke ' + permission_name + ' on ' +
        isnull(schema_name(o.uid)+'.','')+OBJECT_NAME(major_id)+ ' from [' +
        USER_NAME(grantee_principal_id) + ']' as 'revokeStatement'
    ,'grant ' + permission_name + ' on ' +
        isnull(schema_name(o.uid)+'.','')+OBJECT_NAME(major_id)+ ' to ' +
        '[' + USER_NAME(grantee_principal_id) + ']' as 'grantStatement'
FROM sys.database_permissions dp
LEFT OUTER JOIN sysobjects o
    ON o.id = dp.major_id
-- where major_id >= 1  -- ignore sysobjects

order by
    class_desc desc
    ,USER_NAME(grantee_principal_id)
    ,CASE WHEN class = 0 THEN DB_NAME()
         WHEN class = 1 THEN isnull(schema_name(o.uid)+'.','')+OBJECT_NAME(major_id)
         WHEN class = 3 THEN SCHEMA_NAME(major_id) end
    ,permission_name

-- Notable metions --

Select * from INFORMATION_SCHEMA.TABLE_PRIVILEGES

select * from fn_my_permissions(NULL, NULL)

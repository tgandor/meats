SELECT 'drop table ' || table_schema || '.' || TABLE_NAME || ' cascade;' AS q
FROM SVV_TABLES
WHERE svv_tables.table_schema not in ('pg_catalog',
                                      'information_schema')
  AND svv_tables.table_type = 'BASE TABLE'
UNION ALL
SELECT 'drop table ' || table_schema || '.' || TABLE_NAME || ' cascade;' AS q
FROM SVV_TABLES
WHERE svv_tables.table_schema not in ('pg_catalog',
                                      'information_schema')
  AND svv_tables.table_type = 'VIEW' ;

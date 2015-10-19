import pymssql
import sys

def console_choice(values, message='Choose:'):
    print message        
    for name, i in zip(values, xrange(len(values))):
            print '%2d. %s' % (i, name)
    ans = raw_input('Type number, or anything else to cancel: ')
    try:
        idx = int(ans)
        if 0 <= idx < len(values):
            return values[idx]
        return None
    except ValueError:
        return None    
    
class TableAnalyzer(object):
    def __init__(self, choice=console_choice, debug=False, schema='dbo'):
        self.choice = choice
        self.debug = debug
        self.schema = schema
        self.conn =  pymssql.connect(server='.')
        self.cur = self.conn.cursor()                
        self.databases = self._get_row('select [name] from sys.databases')        
        self.database = None
        self.tables = []

    def _exec(self, query):
        if self.debug:
            print >>sys.stderr, 'Running query:', query
        self.cur.execute(query)
    
    def _get_row(self, query):
        results = []
        self._exec(query)
        return [row[0] for row in self.cur]
        
    def db_choice(self):
        self.database = self.choice(self.databases, 'Select database:')
        if self.database:
            self.tables = self._get_row("""
select ST.[name] 
from [{0}].sys.tables ST
join [{0}].sys.schemas SS on SS.schema_id = ST.schema_id
where SS.[name] = '{1}'
""".format(self.database, self.schema))
            
    def table_choice(self):
        return self.choice(self.tables, 'Select table to analyze:')        
    
    def analyze(self, table):
        print '=' * 64
        print 'Analyzing %s.%s ...' % (self.database, table)
        total = int(self._get_row("select count(*) from [{0}].[{1}].[{2}]".format(self.database, self.schema, table))[0])
        print 'Total rows:', total
        columns = self._get_row("""
select SC.[name] 
from [{0}].sys.columns SC 
join [{0}].sys.tables ST on ST.object_id = SC.object_id 
join [{0}].sys.schemas SS on SS.schema_id = ST.schema_id
where ST.[name] = '{1}'
    and SS.[name] = '{2}'
""".format(self.database, table, self.schema))
        print 'Found columns:\n', '\n'.join(columns)
        print '-'*32, 'Done', '-'*32
        
    def main(self):
        while True:
            self.db_choice()
            if self.database is None:
                print 'Bye'
                break
            while True:
                table = self.table_choice()
                if table is None:
                    break
                self.analyze(table)
            
    def __del__(self):
        self.conn.close()
    

if __name__ == '__main__':
    ta = TableAnalyzer()
    ta.main()


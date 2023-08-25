from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import Table

lhs_connstr = open("lhs.txt").read()
rhs_connstr = open("rhs.txt").read()
lhs_query = open("lhs_q.txt").read()
rhs_query = open("rhs_q.txt").read()

lhs_engine = create_engine(lhs_connstr)
rhs_engine = create_engine(rhs_connstr)

lhs_result = lhs_engine.execute(lhs_query)
lhs_rows = {*lhs_result}
lhs_result.close()

rhs_result = rhs_engine.execute(rhs_query)
rhs_rows = {*rhs_result}
rhs_result.close()

common = lhs_rows & rhs_rows
print(f"{len(lhs_rows)=}, {len(rhs_rows)=}, {len(common)=}")

lhs_only = lhs_rows - common
rhs_only = rhs_rows - common
print(f"{lhs_only=}")
print(f"{rhs_only=}")

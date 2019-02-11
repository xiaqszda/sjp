import csv
import sqlite3
import _601sum

db_path = "汇总-2019-01-23-13-30-09.db"
sql_path = 'C:\\Users\\xiatiannan\\Desktop\\新建文件夹 (2)'
file_path = '3303_601_20180000.csv'


conn = sqlite3.connect(db_path)
sql1 = 'drop table if exists ytb601;'
sqls = []
c = conn.cursor()

add = ''
with open(file_path, "r") as f:
    fi = csv.reader(f)
    for i in fi:
        sql_add = 'insert into ytb601('
        if i[0] == '数据处理地':
            sql = 'create table ytb601('
            for j in i:
                if j == '数据处理地':
                    sql = sql + '\'' + j + '\' text not null'
                    add = add + '\'' + j + '\''
                else:
                    sql = sql + ',\'' + j + '\' text not null'
                    add = add + ',\'' + j + '\''
            sql += ");"
            add += ') values ('
            sql_ = sql_add
        if i[0] != '数据处理地':
            sql_add += add
            for j in i:
                sql_add = sql_add + '\'' + j + '\','
            sql_add = sql_add[0:-1] + ');'
            sqls.append(sql_add)


c.execute(sql1)
c.execute(sql)
for j in sqls:
    c.execute(j)

conn.commit()
conn.close()

_601sum.sum_(db_path, sql_path)
import pandas as pd
import sqlite3



sql_ycl = '''
UPDATE ytb601 
SET "三项费用系数" = ( SELECT "行业"."三项费用系数" FROM "行业" WHERE SUBSTR( ytb601."行业代码(GB/T4754-2017)", 1, 2 ) = "行业"."代码" )
WHERE
	(
	SELECT
		"代码" 
	FROM
		"行业" 
	WHERE
		SUBSTR( ytb601."行业代码(GB/T4754-2017)", 1, 2 ) = SUBSTR( "行业"."代码", 1, 2 ) 
	);

update ytb601 
set "三项费用系数" = 0.011
where ytb601."C604-3填报范围" = '1' and SUBSTR("行业代码(GB/T4754-2017)",1,2) = '49';


-- UPDATE ytb601 
-- set "数据处理地"= ('330399' || SUBSTR("数据处理地",7,12))
-- where "数据处理地" like "330305002%";

UPDATE ytb601 
set "数据处理地"= REPLACE(数据处理地,"330305002","330399");



UPDATE ytb601 SET "填报范围" = 'B603-1' WHERE	"B603-1填报范围" = '1';
UPDATE ytb601 SET "填报范围" = 'B603-2' WHERE	"B603-2填报范围" = '1';
UPDATE ytb601 SET "填报范围" = 'C603' WHERE "C603填报范围" = '1';
UPDATE ytb601 SET "填报范围" = 'C604-3' WHERE	"C604-3填报范围" = '1';
UPDATE ytb601 SET "填报范围" = 'E603' WHERE	"E603填报范围" = '1';
UPDATE ytb601 SET "填报范围" = 'S603' WHERE	"S603填报范围" = '1';
UPDATE ytb601 SET "填报范围" = 'X603' WHERE	"X603填报范围" = '1';
UPDATE ytb601 SET "填报范围" = 'F603' WHERE	"F603填报范围" = '1';
'''

def sum_(db_path, sql_path):
	import os
	sqls = []
	c = os.walk(sql_path)
	for i, j, k in c:
		for filename in k:
			if '.sql' in filename:
				with open(i + '\\' + filename,'r', encoding='utf-8') as f:
					ts = f.read()
					sss = [filename[0:-4], ts]
					sqls.append(sss)

	sum2excel(db_path, sqls)

def sum2excel(db_path, sqls):
	excelWriter = pd.ExcelWriter("每日汇总\\一套表汇总.xlsx", engine='openpyxl')
	conn = sqlite3.connect(db_path)
	cor = conn.cursor()
	for i in sql_ycl.split(';'):
		cor.execute(i)
	conn.commit()
	for i,j in sqls:
		res = pd.read_sql(j,conn)
		res.to_excel(excel_writer=excelWriter,sheet_name=i,index=False)
	excelWriter.save()
	excelWriter.close()
	conn.close()


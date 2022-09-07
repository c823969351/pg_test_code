import sqlite3
import pandas as pd

df = pd.DataFrame()

con = sqlite3.connect('ModuleEditTest.db')
#创建一个cursor
cursor = con.cursor()
#获取数据库中的表名
cursor.execute('select name from sqlite_master where type="table"')
#获取所有表名
table_names = cursor.fetchall()
print(table_names)
#获取表
cursor.execute('select * from PicInfoCollection')
#获取KEY
keys = cursor.description
for i in range(len(keys)):
    print(keys[i][0])
#获取表中的数据
data = cursor.fetchall()
#将数据转换为DataFrame
df = pd.DataFrame(data, columns=[keys[i][0] for i in range(len(keys))])
print(df)
#将数据存入本地
df.to_excel('PicInfoCollection.xlsx')
#关闭游标
cursor.close()
#关闭数据库
con.close()

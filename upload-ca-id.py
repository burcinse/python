#-----------------------------------------
# upload-ca-id.py
# 
#
#-----------------------------------------

import os
import MySQLdb
import pandas as pd

#-----------------------------------------

#Exe directory
exe_dir = os.path.dirname(os.path.abspath(__file__))

#-----------------------------------------

#Loading Zip file ad DataFrame
file = os.path.join(exe_dir, "id.zip")
id_local = pd.read_csv(file, compression='zip', header=0, sep='\t', quotechar='"')

#print(id_local)

#Connect with Database
conn = MySQLdb.connect(
user='gemstoo6_jp',
passwd='7abvbhecub63',
host='162.144.142.66',
db='gemstoo6_jp')

cur = conn.cursor()

#Get all CA's ID data from Database
sql = "SELECT *  FROM `CA ID AND SKU TABLE`"
#cur.execute(sql)
id_db = pd.read_sql(sql, conn)
print(id_db)

#Take difference
id_diff = id_local[~id_local['Sku'].isin(id_db['Sku'])]
#Keep only columns necessary and reset index
id_diff = id_diff[['ID','Sku']].reset_index(drop=True)

#print(id_diff)

#Insert only IDs not exist in Database
for i, row in id_diff.iterrows():
    
    #print(i)
    #print(str(row['ID']))
    #print(row['Sku'])
    #print("-----------------")
    sql = "INSERT INTO `CA ID AND SKU TABLE`(`ID`, `Sku`) VALUES ('" + str(row['ID']) + "','" + row['Sku'] + "')"
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()

cur.close()
conn.close()

print("Complete")

import tabula
import pandas as pd
from sqlalchemy.sql.operators import div

df = pd.read_csv("Attendance.csv")
df.columns = ['Name', 'Date ', 'IN/OUT', ]
df.head()
s = df.Name
counts = s.value_counts()

percent = s.value_counts(normalize=True)

percent100 = counts / (180) * 100

'''************************************************************* Students Attendance Record 
******************************************************** '''
cs = pd.DataFrame({'counts': counts,  'Attendance In Percent': percent100})
print(cs)

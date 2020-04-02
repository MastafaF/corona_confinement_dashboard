import pandas as pd

df = pd.read_csv('data/df_confinement.tsv',sep='\t')
df_new = pd.read_csv('../corona_virus_analysis/data/dataframe/df_data.tsv',sep='\t')

df_new_today = df_new[df_new.datetime.str.contains("01-04-2020")]
df_new_today.reset_index(drop = True, inplace = True)

df_total = pd.concat([df_new_today,df], ignore_index = True)
 
df_total.to_csv('../corona_virus_analysis/data/dataframe/df_data.tsv', sep='\t',index=False)

print(df.shape[0] + df_new_today.shape[0] == df_total.shape[0])

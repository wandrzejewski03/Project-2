import pandas as pd

try:
    df = pd.read_csv(
        r'C:\Users\wikto\PycharmProjects\pythonProject\data_analyst\web_scraping\beaufil_soup_course\Files(Project2)\jobs.csv',
        encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(
        r'C:\Users\wikto\PycharmProjects\pythonProject\data_analyst\web_scraping\beaufil_soup_course\Files(Project2)\jobs.csv',
        encoding='ISO-8859-1')

pd.set_option('display.max.rows', None)
pd.set_option('display.max.columns', 8)
pd.set_option('display.width', 500)

df = df.drop(columns='More_info')
df = df.drop_duplicates(subset=['Job', 'Company'])

df = df.replace('Å', 'ń')
df = df.replace('Ã³', 'ó')
df = df.replace('³', 'ł')
df = df.replace('Å', 'ł')


df = df.replace('Å', 'ń', regex=True)
df = df.replace('Ã³', 'ó', regex=True)
df = df.replace('³', 'ł', regex=True)
df = df.replace('Å', 'ł', regex=True)
df = df.replace('ÅódÅº', 'Łódź', regex=True)
df = df.replace('âï¸', '', regex=True)
df = df.replace('zastÄ', '', regex=True)
# df = df.replace('pstwo', '')


df['Job'] = df['Job'].str.replace('(pstwo)', '')
df['Job'] = df['Job'].str.replace('chmurÄ', '')

df['Average_salary'] = df['Average_salary'].str.replace(r'\.*','',regex=True)

# print(df)

output_path = r'C:\Users\wikto\PycharmProjects\pythonProject\data_analyst\web_scraping\beaufil_soup_course\Files(Project2)\jobs(cleaned).csv'
df.to_csv(output_path, index=False, encoding='utf-8')

df_check = pd.read_csv(output_path, encoding='utf-8')
print(df_check)
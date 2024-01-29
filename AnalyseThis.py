import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# file_path = r'C:\Users\leszek.stanislawski\Downloads\Kodilla\Python\Visual\HRDataset.csv'
df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'HRDataset.csv'))

print(df.columns)

df['DateofHire'] = pd.to_datetime(df['DateofHire'])
df['DateofTermination'] = pd.to_datetime(df['DateofTermination'])
df['DaysEmployed'] = (df['DateofTermination'] - df['DateofHire']).dt.days

sns.countplot(x='ManagerID', hue='PerformanceScore', data=df)
plt.xticks(rotation=45, ha='right')
plt.title('Zależność pomiędzy Managerem a PerformanceScore')
plt.show()

df['DaysEmployed'] = (pd.to_datetime(df['DateofTermination']) - pd.to_datetime(df['DateofHire'])).dt.days
recruitment_source_longevity = df.groupby('RecruitmentSource')['DaysEmployed'].mean().sort_values()

recruitment_source_longevity.plot(kind='barh')
plt.xlabel('Średni staż zatrudnienia (dni)')
plt.title('Najlepsze źródła pozyskania pracowników pod względem długości stażu')
plt.show()

sns.boxplot(x='MaritalDesc', y='EmpSatisfaction', data=df)
plt.title('Korelacja stanu cywilnego z zadowoleniem z pracy')
plt.show()

print(df.columns)

current_year = pd.to_datetime('today').year
df['Age'] = current_year - pd.to_datetime(df['DOB']).dt.year
sns.histplot(df['Age'], bins=20, kde=True)
plt.title('Struktura wieku pracowników')
plt.xlabel('Wiek')
plt.show()

sns.scatterplot(x='Age', y='SpecialProjectsCount', data=df)
plt.title('Ilość specjalnych projektów w zależności od wieku pracownika')
plt.xlabel('Wiek')
plt.ylabel('Ilość specjalnych projektów')
plt.show()

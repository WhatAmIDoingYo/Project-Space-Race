import pandas as pd

df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
df.head(10)

df.isnull().sum()/len(df)*100

df.dtypes

print(df['LaunchSite'].value_counts())

print(df['Orbit'].value_counts())

landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)

for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)

bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
bad_outcomes

landing_class = [0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]
print(landing_class)

df['Class']=landing_class
df[['Class']].head(8)

df.head(5)

df["Class"].mean()

df.to_csv("dataset_part_2.csv", index=False)
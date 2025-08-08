import pandas as pd

def makeFeature(df):
    df['date'] = pd.to_datetime(df['date'])

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    df = df.drop(columns=['date'])

    df[df.select_dtypes(['object']).columns] = df.select_dtypes(['object']).astype('category')
    df[df.select_dtypes(['category']).columns] = df.select_dtypes(['category']).apply(lambda x: x.cat.codes)

    df = df.fillna(-1)

    return df

data = pd.read_csv("../../data/merged/data.csv", sep=';')
new_data = pd.read_csv("../../data/merged/new_data.csv", sep=';')

data = makeFeature(data)
new_data = makeFeature(new_data)

data.to_csv("../../data/featured/data.csv", sep=';', index=False)
new_data.to_csv("../../data/featured/new_data.csv", sep=';', index=False)
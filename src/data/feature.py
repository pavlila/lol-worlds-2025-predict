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

winter_daily = pd.read_csv("../../data/merged/winter.csv", sep=';')

winter_daily = makeFeature(winter_daily)

winter_daily.to_csv("../../data/featured/winter.csv", sep=';', index=False)
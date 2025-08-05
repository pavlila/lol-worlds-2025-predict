import pandas as pd
import numpy as np

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

spring = pd.read_csv("../../data/merged/spring.csv", sep=';')
summer = pd.read_csv("../../data/merged/summer.csv", sep=';')
spring_summer = pd.read_csv("../../data/merged/spring_summer.csv", sep=';')
winter_spring = pd.read_csv("../../data/merged/winter_spring.csv", sep=';')
winter_spring_summer = pd.read_csv("../../data/merged/winter_spring_summer.csv", sep=';')

spring = makeFeature(spring)
summer = makeFeature(summer)
spring_summer = makeFeature(spring_summer)
winter_spring = makeFeature(winter_spring)
winter_spring_summer = makeFeature(winter_spring_summer)

spring.to_csv("../../data/featured/spring.csv", sep=';', index=False)
summer.to_csv("../../data/featured/summer.csv", sep=';', index=False)
spring_summer.to_csv("../../data/featured/spring_summer.csv", sep=';', index=False)
winter_spring.to_csv("../../data/featured/winter_spring.csv", sep=';', index=False)
winter_spring_summer.to_csv("../../data/featured/winter_spring_summer.csv", sep=';', index=False)
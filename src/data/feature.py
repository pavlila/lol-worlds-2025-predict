import pandas as pd
from joblib import dump

def makeMirror(df):
    """Rozmnoží dataset: každý zápas A vs B dostane i zrcadlenou verzi B vs A."""

    # Kopie původního dataframe
    df_orig = df.copy()

    # Mirror = prohodíme všechny A/B sloupce
    df_mirror = df.copy()
    
    a_cols = [c for c in df.columns if c.endswith('_A')]
    for a_col in a_cols:
        base = a_col[:-2]
        b_col = f"{base}_B"
        df_mirror[a_col], df_mirror[b_col] = df[b_col], df[a_col]

    # Prohodíme i názvy týmů
    df_mirror['teamA'], df_mirror['teamB'] = df['teamB'], df['teamA']

    # Label musíme zrcadlit → pokud vyhrál A v originálu, v mirroru vyhrál B
    df_mirror['teamA_win'] = 1 - df['teamA_win']

    # Spojíme originál + mirror
    df_out = pd.concat([df_orig, df_mirror], ignore_index=True)

    return df_out
    
def makeDiff(df):
    a_cols = [c for c in df.columns if c.endswith('_A')]
    b_cols = [c for c in df.columns if c.endswith('_B')]

    for a_col in a_cols:
        base = a_col[:-2]
        b_col = f'{base}_B'

        if b_col in b_cols:
            df[f'diff_{base}'] = df[a_col] - df[b_col]
            df[f'ratio_{base}'] = df[a_col] / (df[b_col] + 1e-6)

    df = df.drop(columns=a_cols + b_cols)
    return df

def makeFeature(df):
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df = df.drop(columns=['date'])

    df = makeMirror(df)

    cat_cols = df.select_dtypes(['object']).columns
    df[cat_cols] = df[cat_cols].astype('category')

    decode_maps = {col: dict(enumerate(df[col].cat.categories)) for col in cat_cols}
    dump(decode_maps, "../../data/featured/decode_maps.joblib")

    df[cat_cols] = df[cat_cols].apply(lambda x: x.cat.codes)
    
    df = df.fillna(-1)

    df = makeDiff(df)

    return df

data = pd.read_csv("../../data/merged/data.csv", sep=',')

data = makeFeature(data)

data.to_csv("../../data/featured/data.csv", sep=',', index=False)

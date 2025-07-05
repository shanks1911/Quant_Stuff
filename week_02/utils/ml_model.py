from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def ml_predict_spread(zscore_df):
    zscore_df['Lag1'] = zscore_df['Spread'].shift(1)
    zscore_df['Target'] = (zscore_df['Spread'].shift(-1) > zscore_df['Spread']).astype(int)
    zscore_df.dropna(inplace=True)

    X = zscore_df[['Lag1']]
    y = zscore_df['Target']

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    pred = model.predict(X.tail(1))
    prob = model.predict_proba(X.tail(1))

    return {
        "Prediction": "Long" if pred[0] == 1 else "Short",
        "Confidence": round(prob[0].max(),2)
    }

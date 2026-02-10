def ml_predict_spread(zscore_df):
    df = zscore_df.copy()
    
    df['Lag1'] = df['Spread'].shift(1)
    df['Target'] = (df['Spread'].shift(-1) > df['Spread']).astype(int)
    df.dropna(inplace=True)

    train = df.iloc[:-1]
    test = df.iloc[-1:]

    X_train = train[['Lag1']]
    y_train = train['Target']
    X_test = test[['Lag1']]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)

    return {
        "Prediction": "Long" if pred[0] == 1 else "Short",
        "Confidence": round(prob[0].max(), 2)
    }



# from sklearn.ensemble import RandomForestClassifier
# import pandas as pd

# def ml_predict_spread(zscore_df):
#     zscore_df['Lag1'] = zscore_df['Spread'].shift(1)
#     zscore_df['Target'] = (zscore_df['Spread'].shift(-1) > zscore_df['Spread']).astype(int)
#     zscore_df.dropna(inplace=True)

#     X = zscore_df[['Lag1']]
#     y = zscore_df['Target']

#     model = RandomForestClassifier(n_estimators=100)
#     model.fit(X, y)
#     pred = model.predict(X.tail(1))
#     prob = model.predict_proba(X.tail(1))

#     return {
#         "Prediction": "Long" if pred[0] == 1 else "Short",
#         "Confidence": round(prob[0].max(),2)
#     }

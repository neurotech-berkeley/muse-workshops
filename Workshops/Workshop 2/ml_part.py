model_df = pd.DataFrame({})
df = EEG_data[['name', 'trial number', 'matching condition']].drop_duplicates().reset_index(drop=True)

for i in tqdm(range(len(df))):
    temp_df = EEG_data[(EEG_data['name'] == df['name'][i]) & 
                       (EEG_data['trial number'] == df['trial number'][i]) & 
                       (EEG_data['matching condition'] == df['matching condition'][i])]
    temp_df = pd.pivot_table(temp_df, index=['matching condition', 'subject identifier', 'time'], columns='sensor position', values='sensor value')
    model_df = model_df.append(temp_df)

model_df = model_df.reset_index()
model_df = pd.get_dummies(model_df, columns=['matching condition'])
model_df = model_df.sample(frac=1).reset_index(drop=True) ## shuffle the df
model_df.head()

X_train, X_test, y_train, y_test = train_test_split(model_df.drop(['subject identifier'], axis=1), ## independent variables (X)
                                                    pd.Series(model_df['subject identifier']), ## dependent outcome variable (Y)
                                                    test_size=0.3, random_state=seed)

print('Number of observations in the train set: ' + str(X_train.shape[0]))
print('Number of observations in the test set: ' + str(X_test.shape[0]))


## build XGB model
xgb_model_0 = xgb.XGBClassifier(objective='binary:logistic', max_depth=10, seed=seed) 
xgb_model_0.fit(X_train, y_train) #train the model on train set
y_pred = xgb_model_0.predict(X_test) #predict on test set

print('Classification report:\n')
print(classification_report(y_test, y_pred)) #print the performance
print('Total accuracy score: %.2f' % accuracy_score(y_test, y_pred))


importance_df = pd.DataFrame({'feature': X_train.columns, 'score': xgb_model_0.feature_importances_})
importance_df = importance_df.sort_values(['score'], ascending=False)
importance_df = importance_df.merge(color_scale_df, left_on='feature', right_on='sensor', how='left')
importance_df.loc[importance_df['color'].isnull(), 'color'] = 'rgba(48,203,231,0.7)'


data = go.Bar(x=importance_df['feature'],
              y=importance_df['score'],
              marker=dict(color=importance_df['color']))

layout = go.Layout(title='Feature Importance',
                   xaxis=dict(title='Variable'),
                   yaxis=dict(title='Importance Score (Normalized)'))
fig = go.Figure([data], layout=layout)
iplot(fig)

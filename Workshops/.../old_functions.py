def plot_3d_response(stimulus, df):
    """Function makes 3D surface plots for Sensor Values by Time and Channel for both Groups"""
    condition = (df['subject identifier'] == 'a') & (df['matching condition'] == stimulus)
    x = df['time'][condition]
    y = df['channel'][condition].values
    z = df['sensor value'][condition]

    fig = plt.figure(figsize=(15,10))
    fig.suptitle('Response Values for ' + stimulus + ' Stimulus', fontsize=16)
    ax = fig.add_subplot(2, 1, 1, projection='3d')
    l = ax.plot_trisurf(x, y, z, linewidth=0.2)
    ax.set_title('Alcoholic Group', fontsize=14)
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Channel')
    ax.set_zlabel('Sensor Value (microV)')

    condition = (df['subject identifier'] == 'c') & (df['matching condition'] == stimulus)
    x = df['time'][condition]
    y = df['channel'][condition].values
    z = df['sensor value'][condition]

    ax = fig.add_subplot(2, 1, 2, projection='3d')
    r = ax.plot_trisurf(x, y, z, linewidth=0.2)
    ax.set_title('Control Group', fontsize=14)
    ax.set_xlabel('Time (sec)')
    ax.set_ylabel('Channel')
    ax.set_zlabel('Sensor Value (microV)')
    plt.show()
	
def plot_heatmaps(stimulus, df):
    """Funtion plots two heatmaps for response values for each group side by side."""
    plt.figure(figsize=(15,7))
    plt.subplot(1, 2, 1)
    data = pd.pivot_table(df[['sensor position', 'time', 'sensor value']][df['subject identifier'] == 'a'],
                          values='sensor value', index='sensor position', columns='time')
    ax = sns.heatmap(data, vmin=df['sensor value'].min(), vmax=df['sensor value'].max())
    plt.title('Sensor Values for Alcoholic Group', loc='Center', fontsize=14)

    plt.subplot(1, 2, 2)
    data = pd.pivot_table(df[['sensor position', 'time', 'sensor value']][df['subject identifier'] == 'c'],
                          values='sensor value', index='sensor position', columns='time')
    ax = sns.heatmap(data, vmin=df['sensor value'].min(), vmax=df['sensor value'].max())
    plt.title('Sensor Values for Control Group', loc='Center', fontsize=14)
    plt.suptitle('Heatmap of Sensor Values for ' + stimulus + ' stimulus for each Group', fontsize=16)
    # plt.tight_layout()
    plt.show()
	
def plot_sample_response_time_series(sensor_1, sensor_2, df):
    """Funtion makes a plotly time series plot of two brain areas provided."""
    trial_number_1 = df['trial number'][df['sensor position'] == sensor_1].min()
    trial_number_2 = df['trial number'][df['sensor position'] == sensor_2].min()
    x_1 = df['time'][(df['sensor position'] == sensor_1) & (df['trial number'] == trial_number_1)]
    y_1 = df['sensor value'][(df['sensor position'] == sensor_1) & (df['trial number'] == trial_number_1)]
    x_2 = df['time'][(df['sensor position'] == sensor_2) & (df['trial number'] == trial_number_2)]
    y_2 = df['sensor value'][(df['sensor position'] == sensor_2) & (df['trial number'] == trial_number_2)]
    
    data_1 = go.Scatter(x=x_1,
                        y=y_1,
                        name=sensor_1)
    data_2 = go.Scatter(x=x_2,
                        y=y_2,
                        name=sensor_2)
    data = [data_1, data_2]
    
    layout = go.Layout(title='Response values for ' + df['matching condition'].unique()[0] + ' stimulus',
    xaxis=dict(title='Time (seconds)'),
    yaxis=dict(title='Sensor Value (microV)'))
    
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)
	

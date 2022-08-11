import pandas as pd


# dates
def get_range_from_to(df, start, end):
    start = pd.to_datetime(start, utc=True)
    end = pd.to_datetime(end, utc=True)
    workouts = df[df['creationDate'] >= start]
    workouts = workouts[workouts['creationDate'] <= end]

    return workouts


# dates
def get_on_date(df, date):
    ##  date = pd.to_datetime(dt.date(2022,7,1), utc=True)
    return df[df['creationDate'].dt.date == date]


# dates
def get_on_month_of_year(df, date):
    return df[(df['creationDate'].dt.year == date.year) &
              (df['creationDate'].dt.month == date.month)]


# workouts
def get_workout_by_type(df, workout_type: str):
    return df[df['type'] == workout_type]


# heart rate
def get_heartrate_for_date(hr, start, end):
    hr = hr[hr['startDate'] >= start]
    hr = hr[hr['endDate'] <= end]

    return hr


# heart rates
def get_heartrate_for_workout(heartrate, workout):
    assert 'HeartRate' in heartrate['type'].unique(), "Incorrect dataframe, " \
                                                      "must be Record " \
                                                      "dataframe "

    return get_heartrate_for_date(heartrate, workout['startDate'].item(),
                                  workout['endDate'].item())


# cleaning
def remove_outliers(df, columns, n_std):
    for col in columns:
        # print('Working on column: {}'.format(col))
        mean = df[col].mean()
        sd = df[col].std()
        df = df[(df[col] <= mean + (n_std * sd))]

    return df


# cleaning
def filter_type(df: pd.DataFrame, record_type: str):
    return df[df['type'] == record_type]

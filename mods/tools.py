import pandas as pd
import datetime as dt


# create
def get_record_type(records, cond):
    return records[cond]


# dates
def get_range_from_to(df, start, end):  # TODO utc affect range
    start = pd.to_datetime(start, utc=True)
    end = pd.to_datetime(end, utc=True)
    data = df[df['creationDate'] >= start]
    data = data[data['creationDate'] <= end]

    return data


# dates
def get_on_date(df, year: int, month: int, day: int):
    date = pd.to_datetime(dt.date(year, month, day), utc=True)
    return df[df['creationDate'].dt.date == date]


# dates
def get_on_month_of_year(df, year: int, month: int, day=1):
    date = pd.to_datetime(dt.date(year, month, day), utc=True)
    return df[(df['creationDate'].dt.year == date.year) &
              (df['creationDate'].dt.month == date.month)]


# TODO all stats have value, date, and unit as important features;  probably want to return series instead of df
def get_daily_stat(records, year: int, month: int, day: int, match: str):
    cond = records['type'] == match
    data = get_record_type(records, cond)
    daily = get_on_date(data, year, month, day)
    return daily


def get_monthly_stat(records, year: int, month: int, match: str):
    cond = records['type'] == match
    data = get_record_type(records, cond)
    monthly = get_on_month_of_year(data, year, month)
    return monthly


# TODO split into their own energy types and make a new total_cal method to
# TODO keep consistency across get_monthly of all kinds of types
# calories
def get_daily_calories(records, year: int, month: int, day: int):
    cond = (records['type'] == 'BasalEnergyBurned') | \
           (records['type'] == 'ActiveEnergyBurned')
    calories = get_record_type(records, cond)
    total_cal = get_on_date(calories, year, month, day).value.sum()
    return total_cal


# calories
def get_monthly_calories(records, year: int, month: int):
    cond = (records['type'] == 'BasalEnergyBurned') | \
           (records['type'] == 'ActiveEnergyBurned')
    calories = get_record_type(records, cond)
    total_cal = get_on_month_of_year(calories, year, month).value.sum()
    return total_cal


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

import pandas as pd
import datetime as dt

# TODO sum monthly
# TODO merge workout and record tables?
# TODO split Records types into their own csv files
# TODO set workout related functions in a separate file ?
FEATURES = ['type', 'value', 'unit', 'creationDate', 'startDate', 'endDate']
RECORD_TYPES = ['Height', 'BodyMass', 'HeartRate', 'RespiratoryRate',
                'StepCount',
                'DistanceWalkingRunning', 'BasalEnergyBurned',
                'ActiveEnergyBurned', 'FlightsClimbed', 'AppleExerciseTime',
                'DistanceSwimming', 'SwimmingStrokeCount', 'RestingHeartRate',
                'VO2Max', 'WalkingHeartRateAverage', 'HeadphoneAudioExposure',
                'WalkingDoubleSupportPercentage', 'SixMinuteWalkTestDistance',
                'AppleStandTime', 'WalkingSpeed', 'WalkingStepLength',
                'WalkingAsymmetryPercentage', 'SleepDurationGoal',
                'AppleWalkingSteadiness', 'SleepAnalysis', 'AppleStandHour',
                'MindfulSession', 'HeartRateVariabilitySDNN']


# create
def get_type(df: pd.DataFrame, cond: pd.Series) -> pd.DataFrame:
    """
    Filters dataframe based around the 'type' feature
    :param df: Record dataFrame
    :param cond: boolean Series
    :return: dataframe of a specific 'type'
    """
    return df[cond]


# dates
def get_range_from_to(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp)\
        -> pd.DataFrame:
    """
    In any dataframe with a 'creationDate' feature return rows within a specific
    date range
    :param df: dataFrame with 'creationDate' feature
    :param start: timestamp for the range start (inclusive)
    :param end: timestamp for the range end (inclusive)
    :return: dataframe with rows within the date range
    """
    assert 'creationDate' in df.columns, 'DataFrame does not have column ' \
                                         '"creationDate"'
    start = pd.to_datetime(start, utc=True)
    end = pd.to_datetime(end, utc=True)
    data = df[df['creationDate'] >= start]
    data = data[data['creationDate'] <= end]

    return data


# dates
def get_on_date(df: pd.DataFrame, year: int, month: int, day: int) \
        -> pd.DataFrame:
    """
    dataframe for data on a given day
    :param df: dataFrame with 'creationDate' feature
    :param year: year to filter
    :param month: month to filter
    :param day: day to filter
    :return: dataFrame with rows for a given date
    """
    assert 'creationDate' in df.columns, 'DataFrame does not have column ' \
                                         '"creationDate"'
    date = pd.to_datetime(dt.date(year, month, day), utc=True)
    return df[df['creationDate'].dt.date == date]


# dates
def get_on_month_of_year(df: pd.DataFrame, year: int, month: int) \
        -> pd.DataFrame:
    """
    dataframe for date onf a given month within a year
    :param df: dataFrame with 'creationDate' feature
    :param year: year to filter
    :param month: month to filter
    :return: dataFrame with rows for a given month in a year
    """
    assert 'creationDate' in df.columns, 'DataFrame does not have column ' \
                                         '"creationDate"'
    date = pd.to_datetime(dt.date(year, month, 1), utc=True)
    return df[(df['creationDate'].dt.year == date.year) &
              (df['creationDate'].dt.month == date.month)]


# stats
def get_daily_stat(records: pd.DataFrame, year: int, month: int, day: int,
                   match: str) -> pd.DataFrame:
    """
    daily stats for a selected date on a given 'type'
    :param records: Record dataFrame
    :param year: date year
    :param month: date month
    :param day: date day
    :param match: str corresponding to the 'type' column value
    :return: dataFrame with rows for a given date with chosen 'type'
    """
    assert match in RECORD_TYPES, match + ' not a record type'
    cond = records['type'] == match
    data = get_type(records, cond)
    daily = get_on_date(data, year, month, day)
    return daily[FEATURES]


# stats
def get_monthly_stat(records: pd.DataFrame, year: int, month: int,
                     match: str) -> pd.DataFrame | None:
    """
    monthly stats for a selected date ona given 'type'
    :param records: Record dateFrame
    :param year: date year
    :param month: date month
    :param match: str corresponding to the 'type' column value
    :return: dateFrame with rows for a given month in a year with a
    chosen 'type'
    """
    assert match in RECORD_TYPES, match + ' not a record type'
    cond = records['type'] == match
    data = get_type(records, cond)
    monthly = get_on_month_of_year(data, year, month)
    return monthly[FEATURES]


# calories
def get_daily_calories(records: pd.DataFrame, year: int, month: int, day: int) \
        -> float:
    """
    alternate method to getting daily calorie stats
    :param records: Record dataFrame
    :param year: date year
    :param month: date month
    :param day: date day
    :return: float for total calories burned on a given day
    """
    cond = (records['type'] == 'BasalEnergyBurned') | \
           (records['type'] == 'ActiveEnergyBurned')
    calories = get_type(records, cond)
    total_cal = get_on_date(calories, year, month, day).value.sum()
    return total_cal


# calories
def get_monthly_calories(records: pd.DataFrame, year: int, month: int) -> float:
    """
    alternate method to getting monthly calorie stats
    :param records: Record dataFrame
    :param year: date year
    :param month: date month
    :return: float for total calories burned on a given month in a year
    """
    cond = (records['type'] == 'BasalEnergyBurned') | \
           (records['type'] == 'ActiveEnergyBurned')
    calories = get_type(records, cond)
    total_cal = get_on_month_of_year(calories, year, month).value.sum()
    return total_cal


# heart rate
def get_heartrate_for_workout(records: pd.DataFrame, workout: pd.Series) \
        -> pd.DataFrame:
    """
    Get heartrate data for a chosen workout
    :param records: Records dataFrame
    :param workout: singular workout from Workout dataFrame (a row)
    :return: dataFrame with heartrate data
    """
    cond = records['type'] == 'HeartRate'
    heartrate = get_type(records, cond)

    def get_heartrate_for_date(hr, start, end):
        hr = hr[hr['startDate'] >= start]
        hr = hr[hr['endDate'] <= end]

        return hr

    # workout item must be 1D, use
    return get_heartrate_for_date(heartrate, workout['startDate'],
                                  workout['endDate'])


def get_value(record: pd.Series) -> float:
    """
    'value' feature from a given record
    :param record: Series, a single row entry in the dataFrame
    :return: float 'value'
    """
    return record['value']


def get_unit(record: pd.Series) -> str:
    """
    'unit' feature from a given record
    :param record: Series, a single row entry in the dataFrame
    :return: str 'unit'
    """
    return record['unit']


def get_duration(workout: pd.Series) -> float:
    """
    'duration' feature from a given workout
    :param workout: Series, single row entry in the DataFrame
    :return: float 'duration'
    """
    return workout['duration']


def get_totalDistance(workout: pd.Series) -> float:
    """
    'totalDistance' feature from a given workout
    :param workout: Series, single row entry in the DataFrame
    :return: float 'totalDistance'
    """
    return workout['totalDistance']


def get_totalEnergyBurned(workout: pd.Series) -> float:
    """
    'totalEnergyBurned' feature from a given workout
    :param workout: Series, single row entry in the DataFrame
    :return: float 'totalEnergyBurned'
    """
    return workout['totalEnergyBurned']

# math


def remove_outliers(df: pd.DataFrame, columns: list, n_std: float) \
        -> pd.DataFrame:
    """
    remove outliers within specified columns
    :param df: dataFrame to remove outliers from
    :param columns: columns to remove outliers from
    :param n_std: number of standard deviations to determine whether outlier
     should be removed or not
    :return:
    """
    for col in columns:
        # print('Working on column: {}'.format(col))
        mean = df[col].mean()
        sd = df[col].std()
        df = df[(df[col] <= mean + (n_std * sd))]

    return df

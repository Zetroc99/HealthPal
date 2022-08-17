import pandas as pd
import datetime as dt
from pandas import DataFrame

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
def get_record_type(records, cond) -> pd.DataFrame:
    return records[cond]


# dates
def get_range_from_to(df, start, end) -> pd.DataFrame:
    start = pd.to_datetime(start, utc=True)
    end = pd.to_datetime(end, utc=True)
    data = df[df['creationDate'] >= start]
    data = data[data['creationDate'] <= end]

    return data


# dates
def get_on_date(df, year: int, month: int, day: int) -> pd.DataFrame:
    date = pd.to_datetime(dt.date(year, month, day), utc=True)
    return df[df['creationDate'].dt.date == date]


# dates
def get_on_month_of_year(df, year: int, month: int, day=1) -> pd.DataFrame:
    date = pd.to_datetime(dt.date(year, month, day), utc=True)
    return df[(df['creationDate'].dt.year == date.year) &
              (df['creationDate'].dt.month == date.month)]


# stats
def get_daily_stat(records, year: int, month: int, day: int,
                   match: str) -> DataFrame | None:
    if match in RECORD_TYPES:
        cond = records['type'] == match
        data = get_record_type(records, cond)
        daily = get_on_date(data, year, month, day)
        return daily[FEATURES]
    return None


# stats
def get_monthly_stat(records, year: int, month: int,
                     match: str) -> pd.DataFrame | None:
    if match in RECORD_TYPES:
        cond = records['type'] == match
        data = get_record_type(records, cond)
        monthly = get_on_month_of_year(data, year, month)
        return monthly[FEATURES]
    return None


# calories
def get_daily_calories(records, year: int, month: int, day: int) -> float:
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


# TODO set workout related functions in a separate file ?
# workouts
def get_workout_by_type(df, workout_type: str):
    return df[df['type'] == workout_type]


# workouts
def get_heartrate_for_workout(records, workout):
    cond = records['type'] == 'HeartRate'
    heartrate = get_record_type(records, cond)

    def get_heartrate_for_date(hr, start, end):
        hr = hr[hr['startDate'] >= start]
        hr = hr[hr['endDate'] <= end]

        return hr
# workout item must be 1D, use
    return get_heartrate_for_date(heartrate, workout['startDate'].item(),
                                  workout['endDate'].item())

# TODO get workouts on day
# TODO get workouts on month
# TODO get heartrate from _ to _ ?

# TODO get values (Records) -> series
# TODO get duration (Workouts) -> float
# TODO get totalDistance (Workouts) -> float
# TODO get totalEnergyBurned (Workouts) -> float
# TODO merge workout and record tables?
# TODO split Records types into their own csv files


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

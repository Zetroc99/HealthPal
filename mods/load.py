import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("./data/apple_health_export/export.xml")
root = tree.getroot()
BAD_FEATURES = ['sourceVersion', 'device']


# TODO update_df when a new xml file with updated values is added
def create_df(record_type: str):
    """
    'Record' or 'Workout'
    :param record_type: str of the above
    :return: DataFrame
    """
    data_list = [x.attrib for x in root.iter(record_type)]
    data_df = pd.DataFrame(data_list)

    return data_df


def watch_fix(df: pd.DataFrame):
    """
    Fixes Apple Watch string value
    :param df: DataFrame with 'sourceName' feature
    :return: None
    """
    df.loc[df['sourceName'] == 'Marlon’s Apple\xa0Watch',
           'sourceName'] = "Apple Watch"


def clean_record_df(records: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaned Record DataFrame
    :param records: Record DataFrame
    :return: clean
    """
    # to datetime
    for col in ['creationDate', 'startDate', 'endDate']:
        records[col] = pd.to_datetime(records[col], utc=True)

    records['creationDate'] = pd.to_datetime(records['creationDate'].apply(
        lambda t: t.date()), utc=True)

    # value to numeric or nan
    records['value'] = pd.to_numeric(records['value'], errors='coerce')
    records['value'] = records['value'].fillna(1.0)

    # shorter abbreviations
    records['type'] = records['type'].str.replace('HKQuantityTypeIdentifier', '')
    records['type'] = records['type'].str.replace('HKCategoryTypeIdentifier', '')
    records['type'] = records['type'].str.replace('HKDataType', '')

    watch_fix(records)

    return records.drop(columns=BAD_FEATURES)


def clean_workout_df(workouts: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaned Workout DataFrame
    :param workouts: Workout DataFrame
    :return: clean
    """
    workouts['workoutActivityType'] = workouts[
        'workoutActivityType'].str.replace('HKWorkoutActivityType', '')
    workouts = workouts.rename({"workoutActivityType": "type"}, axis=1)

    # to datetime
    for col in ['creationDate', 'startDate', 'endDate']:
        workouts[col] = pd.to_datetime(workouts[col], utc=True)

    workouts['creationDate'] = pd.to_datetime(workouts['creationDate'].apply(
        lambda t: t.date()), utc=True)

    # string to numeric
    workouts['duration'] = pd.to_numeric(workouts['duration'])
    workouts['totalEnergyBurned'] = pd.to_numeric(workouts['totalEnergyBurned'])
    workouts['totalDistance'] = pd.to_numeric(workouts['totalDistance'])

    watch_fix(workouts)

    return workouts.drop(columns=BAD_FEATURES)

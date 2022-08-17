import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("./data/apple_health_export/export.xml")
root = tree.getroot()
BAD_FEATURES = ['sourceVersion', 'device']


# TODO drop  sourceVersion, device
def create_df(record_type: str):
    """
    'Record' or 'Workout'
    :param record_type:
    :return:
    """
    data_list = [x.attrib for x in root.iter(record_type)]
    data_df = pd.DataFrame(data_list)

    return data_df


def watch_fix(df: pd.DataFrame):
    df.loc[df['sourceName'] == 'Marlon’s Apple\xa0Watch',
           'sourceName'] = "Apple Watch"


def clean_record_df(df: pd.DataFrame):
    # to datetime
    for col in ['creationDate', 'startDate', 'endDate']:
        df[col] = pd.to_datetime(df[col], utc=True)

    # value to numeric or nan
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['value'] = df['value'].fillna(1.0)

    # shorter abbreviations
    df['type'] = df['type'].str.replace('HKQuantityTypeIdentifier', '')
    df['type'] = df['type'].str.replace('HKCategoryTypeIdentifier', '')
    df['type'] = df['type'].str.replace('HKDataType', '')

    watch_fix(df)

    return df.drop(BAD_FEATURES)


def clean_workout_df(df: pd.DataFrame):
    df['workoutActivityType'] = df[
        'workoutActivityType'].str.replace('HKWorkoutActivityType', '')
    df = df.rename({"workoutActivityType": "type"}, axis=1)

    # to datetime
    for col in ['creationDate', 'startDate', 'endDate']:
        df[col] = pd.to_datetime(df[col], utc=True)

    # string to numeric
    df['duration'] = pd.to_numeric(df['duration'])
    df['totalEnergyBurned'] = pd.to_numeric(df['totalEnergyBurned'])
    df['totalDistance'] = pd.to_numeric(df['totalDistance'])

    watch_fix(df)

    return df.drop(BAD_FEATURES)





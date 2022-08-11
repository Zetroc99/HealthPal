import mods

records = mods.load.create_df('Record')
workouts = mods.load.create_df('Workout')

records = mods.load.clean_record_df(records)
workouts = mods.load.clean_workout_df(workouts)



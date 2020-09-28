import pathlib
import pandas

def read_log_txt(path: pathlib.Path, **keyargs):
    df = pandas.read_csv(
        path,
        delimiter='\t',
        skiprows=6,
        usecols=list(range(11))[2:],
        names=[
#           'participant_name',
#           'participant_ID',
            'session_type',
            'event_name',
            '???',
            'response',
            'key',
            'mouse_X',
            'mouse_Y',
            'error_code',
            'reaction_time',
        ]
    )
    for key, item in keyargs.items():
        df[key] = item
        print(key, item)

    # set session types name
    df.loc[df.session_type<=5, 'session_type_name'] = 'standard'
    df.loc[df.session_type>5, 'session_type_name'] = 'deviant'

    #set Hit or False
    df.loc[(df.session_type<=5) & (df.response=='Left'),'outcome'] = 'Correct reject'
    df.loc[(df.session_type<=5) & (df.response=='Right'),'outcome'] = 'False alarm'
    df.loc[(df.session_type>5) & (df.response=='Left'),'outcome'] = 'Miss'
    df.loc[(df.session_type>5) & (df.response=='Right'),'outcome'] = 'Hit'

    return df[df.response.notna()]

if __name__ == '__main__':
    import argparse
    import itertools

    parser = argparse.ArgumentParser()
    parser.add_argument('log_dir', type=pathlib.Path, help='a path include answer log')
    args = parser.parse_args()

    assert args.log_dir.exists()

    log_df_list = list()
    for pid_date_path, i in itertools.product(args.log_dir.glob('*'), range(3)):
        if pid_date_path.is_file():
            continue
        pid_date = pid_date_path.stem
        pid, date = pid_date.split('_')
        print(pid, date)
        df = read_log_txt(
            pid_date_path/'42_active_{}.txt'.format(i+1),
            participant_id = pid,
            experiment_date = date,
            stem = pid_date,
            block = str(i+1)
        )
        log_df_list.append(df)

    pandas.concat(log_df_list).to_csv(args.log_dir/'answers.csv')
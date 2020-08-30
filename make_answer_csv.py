import pathlib
import pandas

def read_log_txt(path: pathlib.Path, participant_id: str, block: int):
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
    df['participant_id'] = participant_id
    df['block'] = block

    # set session types name
    df.loc[df.session_type<=5, 'session_type_name'] = 'standard'
    df.loc[df.session_type>5, 'session_type_name'] = 'deviant'

    #set Hit or False
    df.loc[(df.session_type<=5) & (df.response=='Left'),'outcome'] = 'Hit'
    df.loc[(df.session_type<=5) & (df.response=='Right'),'outcome'] = 'Miss'
    df.loc[(df.session_type>5) & (df.response=='Left'),'outcome'] = 'False alarm'
    df.loc[(df.session_type>5) & (df.response=='Right'),'outcome'] = 'Correct reject'

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
        pid = pid_date.split('_')[0]
        df = read_log_txt(
            pid_date_path/'42_active_{}.txt'.format(i+1),
            pid,
            i+1
        )
        log_df_list.append(df)

    pandas.concat(log_df_list).to_csv(args.log_dir/'answers.csv')
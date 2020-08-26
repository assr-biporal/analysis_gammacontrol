import mne
def raw_processing(raw: mne.io.Raw, *, low_pass=None, high_pass=None, notch=None, montage=None):
    raw.filter(high_pass, low_pass)
    if notch is not None:
        raw.notch_filter(notch)
    if montage is not None:
        raw.set_montage(montage)
    if channel_types is not None:
        raw.set_channel_types(channel_types)
    return raw

def ica_apply(raw: mne.io.Raw, *, )

if __name__ == '__main__':
    import pathlib
    import sys
    raw_path = pathlib.Path(sys.argv[1])

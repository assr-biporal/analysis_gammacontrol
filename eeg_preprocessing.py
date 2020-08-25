import collections
import itertools
import json
import multiprocessing
import pathlib

import matplotlib.pyplot as plt
import mne
mne.set_log_level(False)
import numpy

#EEG montage
BIOSEMI_MONTAGE = mne.channels.make_standard_montage('biosemi64')
#define types of extra channels
EXGCHANNELS_DICT = {
    "EXG1":"misc",
    "EXG2":"misc",
    "EXG3":"eog",
    "EXG4":"eog",
    "EXG5":"eog",
    "EXG6":"misc",
    "EXG7":"misc"
}
#define events
EVENTS_DICT = {
    "standard":1024,
    "deviant":2048
}

def read_raw(bdf_path: pathlib.Path, exclude: list):
    raw = mne.io.read_raw_bdf(bdf_path, exclude=['EXG8']+exclude, preload=True)
    raw.filter(1., 100.)
    raw.notch_filter(60.)
    raw.set_channel_types(EXGCHANNELS_DICT)
    raw.set_montage(BIOSEMI_MONTAGE)
    return bdf_path.stem, raw

def fit_ica(name: str, raw: mne.io.Raw):
    ica = mne.preprocessing.ICA(n_components=0.99)
    ica.fit(raw)
    return name, ica

def make_epochs(name: str, raw: mne.io.Raw, ica):
    exclude_components = list()
    for exg_name, exg_type in EXGCHANNELS_DICT.items():
        if exg_type == 'eog':
            eog_indices, eog_scores = ica.find_bad_eog(raw, ch_name=exg_name)
            exclude_components.append(numpy.argmax(numpy.abs(eog_scores)))
    applied_raw = ica.apply(raw.copy(), exclude=list(set(exclude_components)))
    return name, mne.Epochs(
        applied_raw,
        mne.find_events(applied_raw),
        event_id=EVENTS_DICT,
        tmin=-0.4, tmax=0.7,
        reject=dict(eeg=200e-6),
        preload=True
    )

def main(dir_path: pathlib.Path, exclude: list):
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        raw_dict = collections.OrderedDict(
            pool.starmap(read_raw, [(bdf_path, exclude) for bdf_path in dir_path.glob('*.bdf')])
        )
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        ica_dict = collections.OrderedDict(
            pool.starmap(fit_ica, [(name, raw) for name, raw in raw_dict.items()])
        )
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        epochs_dict = collections.OrderedDict(
            pool.starmap(make_epochs, [(name, raw_dict[name], ica_dict[name]) for name in raw_dict.keys()])
        )
    
if __name__ == '__main__':
    import sys
    main(pathlib.Path(sys.argv[1]), [])
    
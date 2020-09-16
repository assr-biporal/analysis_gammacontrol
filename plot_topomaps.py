import pathlib
import h5py#for confirm to save *-tfr.h5
import matplotlib.pyplot as plt
import mne



if __name__ == '__main__':
    import argparse
    import numpy
    

    parser = argparse.ArgumentParser()
    parser.add_argument('epochs_dirpath', type=pathlib.Path)
    parser.add_argument('freq_start', type=float, default=5.)
    parser.add_argument('freq_end', type=float, default=60.)
    parser.add_argument('freq_step', type=float, default=1.)

    args = parser.parse_args()

    freqs = numpy.arange(args.freq_start, args.freq_end, args.freq_step)

    for condition in ['passive', 'active']:
        epochs = mne.concatenate_epochs(
            [mne.read_epochs(args.epochs_dirpath/(condition + str(i+1) + '-epo.fif.gz'), )]
        )
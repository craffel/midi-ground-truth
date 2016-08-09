# midi-ground-truth

This repository contains the code and data for the paper ["Extracting Ground Truth Information from MIDI Files: A MIDIfesto"](http://colinraffel.com/publications/ismir2016extracting.pdf).
All of the experiments are contained within the IPython notebooks, and the data lives in the `data` directory.
Apart from Python dependencies, you also need to place the Beatles .wav files used to create the Isophonics annotations in `data/wav`.
If you do not have a source for these files, please contact me directly.

Dependencies:

- [`mir_eval`](https://github.com/craffel/mir_eval)
- [`pretty_midi`](https://github.com/craffel/pretty-midi)
- [`numpy`](http://www.numpy.org)
- [`librosa`](https://github.com/librosa/librosa)
- [`vamp`](http://www.vamp-plugins.org/vampy.html)
- [`tabulate`](https://pypi.python.org/pypi/tabulate)
- [`djitw`](https://github.com/craffel/djitw/tree/master/djitw)
- [`joblib`](https://pypi.python.org/pypi/joblib)
- [`matplotlib`](http://matplotlib.org)
- [`seaborn`](https://stanford.edu/~mwaskom/software/seaborn/)

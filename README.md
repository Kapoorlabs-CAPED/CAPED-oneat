# oneat

[![License BSD-3](https://img.shields.io/pypi/l/oneat.svg?color=green)](https://github.com/Kapoorlabs-CAPED/oneat/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/oneat.svg?color=green)](https://pypi.org/project/oneat)
[![Python Version](https://img.shields.io/pypi/pyversions/oneat.svg?color=green)](https://python.org)
[![tests](https://github.com/Kapoorlabs-CAPED/oneat/workflows/tests/badge.svg)](https://github.com/Kapoorlabs-CAPED/oneat/actions)
[![codecov](https://codecov.io/gh/Kapoorlabs-CAPED/oneat/branch/main/graph/badge.svg)](https://codecov.io/gh/Kapoorlabs-CAPED/oneat)


Action classification for TZYX shaped images, Static classification for TYX shaped images

----------------------------------

This [caped] package was generated with [Cookiecutter] using [@caped]'s [cookiecutter-template] template.



## Installation

You can install `oneat` via [pip]:

    pip install oneat



To install latest development version :

    pip install git+https://github.com/Kapoorlabs-CAPED/oneat.git


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"oneat" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.


[pip]: https://pypi.org/project/pip/
[caped]: https://github.com/Kapoorlabs-CAPED
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@caped]: https://github.com/Kapoorlabs-CAPED
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-template]: https://github.com/Kapoorlabs-CAPED/cookiecutter-template

[file an issue]: https://github.com/Kapoorlabs-CAPED/oneat/issues

[caped]: https://github.com/Kapoorlabs-CAPED/
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/


## Algorithm for finding mitotic cells in TZYX datasets


### Program structure

We use hydra library to separate the parameters of the code from the actual file that contains the runnable code. We do so to minimize the interaction with the actual script/file/interactive code where the users do not have to change any lines to specify the paths/filenames/parameters. The [configuration file to modify the parameters](https://github.com/Kapoorlabs-CAPED/Mari_Scripts_Server/blob/main/conf/config_oneat.yaml). The params_train contains the training parameters for the hyperparameters of the network, these parameters are set once and for all and are not learned during the training process, hence the name hyperparameters. The params_predict contains the parameters needed for model prediction such as the number of tiles, event threshold and confidence to veto the events below the threshold. The trainclass contains the training class used by oneat and is input as a string. For VollNet (Resnet based) the training class is NEATVollNet, for DenseVollNet (Densenet based) the training class is DenseVollNet. The defaults provides the filename and the paths, depending on where the data is you only have to select the path file which is supplied for local paths/ovh server paths/aws paths. 
### The training data

### Program to create the training data

### ResNet and DenseNet based VollNet and DenseVollNet architectures


### Program to train the model on a GPU based machine


### Visualizing training loss and accuracy with Tensorboard

Oneat supports visualization of the training loss, accuracy and other training metrics using tensorboard. Tensorboard can be started from the same directory from where you launched the training script/interactive program for training. Inside that folder you will find an **outputs** directory, inside it is a timestamped directory of logs for the tensorboard, for example the directory is named 08-21-02/ then launch tensorboard with the following command from inside the outputs directory: `tensorboard --logdir 08-21-02/`. Tensorboard will print a localhost url to copy and paste in the browser for example `http://localhost:6007/`, clicking on the menu item of scalars shows the loss and accuracy plots for the training epochs. You can refresh the page to update the curves if it does not happen automatically.
from .NEATModels import *
from .NEATUtils import *
from .version import __version__
from csbdeep.utils.tf import keras_import
from . import NEATDynamic, NEATSynamic

from oneat.pretrained import register_model, register_aliases, clear_models_and_aliases

get_file = keras_import('utils', 'get_file')


clear_models_and_aliases(NEATDynamic, NEATSynamic)

register_model(NEATSynamic,   'Cellsplitdetectorbrightfield',  'https://zenodo.org/record/6481021/files/Cellsplitdetectorbrightfield.h5', '0c6ba49c1ba0eb91819af40460fb66cb',
                               'Cellsplitcordhelaflou'         ,   'https://zenodo.org/record/6481021/files/Cellsplitcordhelaflou.json', 'aed21cb69d6fb8be32c47f78a39d32f5',
                                'Cellsplitcategorieshelaflou'  , 'https://zenodo.org/record/6481021/files/Cellsplitcategorieshelaflou.json', '7a67a83f08fb1add3c1b1a3e0eeec773',
                                 'Cellsplitdetectorbrightfield_Parameter' , 'https://zenodo.org/record/6481021/files/Cellsplitdetectorbrightfield_Parameter.json', '266e3e7fa7587d53d62ae0492482a1bc'  )  



register_model(NEATSynamic,   'Cellsplitdetectorhdpc',  'https://zenodo.org/api/files/e9c36959-f379-48f6-ab0d-29f26bf446e0/Cellsplitdetectorhdpc.h5', '701d7fc8494b66a73b024f3d3c3d3dad',
                               'Cellsplitcordhelaflou'         ,   'https://zenodo.org/record/6481021/files/Cellsplitcordhelaflou.json', 'aed21cb69d6fb8be32c47f78a39d32f5',
                                'Cellsplitcategorieshelaflou'  , 'https://zenodo.org/record/6481021/files/Cellsplitcategorieshelaflou.json', '7a67a83f08fb1add3c1b1a3e0eeec773',
                                 'Cellsplitdetectorhdpc_Parameter' , 'https://zenodo.org/api/files/9fd99dcc-1716-403f-aef5-f64629873aa8/Cellsplitdetectorhdpc_Parameter.json', '556f0ce063a4cacda6b9f27ae7aae69b'  )  

register_aliases(NEATSynamic, 'Cellsplitdetectorbrightfield',  'Cellsplitdetectorbrightfield')
register_aliases(NEATSynamic, 'Cellsplitdetectorhdpc',  'Cellsplitdetectorhdpc')


del register_model, register_aliases, clear_models_and_aliases


def abspath(path):
    import os
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, path)



def test_image_brightfield(target):
    from tifffile import imread, imwrite
    import os
    url = "https://zenodo.org/record/6480142/files/20210904_TL2%20-%20R05-C03-F0_ch_2.tif"
    hash = "67e13fa4df301dfe2c2a57f785aedada"
    fname = abspath(get_file(fname='brightfield', origin=url, file_hash=hash))
    image = imread(fname)
    Name = os.path.basename(os.path.splitext(fname)[0])
    imwrite(target + '/' + Name + '.tif', image.astype('float32'))
    return fname  

def test_image_hdpc(target):
    from tifffile import imread, imwrite
    import os
    url = "https://zenodo.org/api/files/9fd99dcc-1716-403f-aef5-f64629873aa8/20210904_TL2%20-%20R05-C03-F0_ch_1.tif"
    hash = "ec6fde9a27a627866e88d44a6d98f41e"
    fname = abspath(get_file(fname='hdpc', origin=url, file_hash=hash))
    image = imread(fname)
    Name = os.path.basename(os.path.splitext(fname)[0])
    imwrite(target + '/' + Name + '.tif', image.astype('float32'))
    return fname  
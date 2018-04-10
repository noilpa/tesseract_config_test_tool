try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import numpy as np
import shutil
import os
import difflib
from pprint import pprint

counter = 0

# change for your tesseract path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

output_folder = './out'
ideal_file_path = './ideal.txt'

def test_one(img, parameters):

    global counter
    global output_folder

    for parameter in parameters:

        start = parameter['start']
        stop  = parameter['stop']
        step  = parameter['step']
        name  = parameter['name']

        for value in np.arange(start, stop, step):
            config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" -c {0}={1}'.format( \
                name, value)

            with open('./out/out{0}.txt'.format(counter), 'w') as f:

                # Print options in file start
                print(name, value, '\n', file=f)

                # Print recognition in file
                print(pytesseract.image_to_string(img, lang='rus', config=config), file=f)

            counter += 1


def test_one_with_preset(img, parameter_with_preset):

    global counter
    global output_folder

    start = parameter_with_preset['parameter']['start']
    stop = parameter_with_preset['parameter']['stop']
    step = parameter_with_preset['parameter']['step']
    name = parameter_with_preset['parameter']['name']

    preset_options = ''

    for item in parameter_with_preset['preset']:
        preset_options = preset_options + str(item['name']) + '=' + str(item['value']) + ' '

    preset_options.strip()

    for value in np.arange(start, stop, step):
        config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" -c {0}={1} {2}'.format( \
            name, value, preset_options)
        with open('{0}/out{1}.txt'.format(output_folder, counter), 'w') as f:
            # Print options in file start
            print(name, value, file=f)
            print(preset_options, '\n', file=f)

            # Print recognition in file
            print(pytesseract.image_to_string(img, lang='rus', config=config), file=f)

        counter += 1


def correlation(img, first_param, second_param):

    global counter
    global output_folder

    for first in np.arange(first_param['start'], first_param['stop'], first_param['step']):
        for second in np.arange(second_param['start'], second_param['stop'], second_param['step']):
            config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" -c {0}={1} {2}={3}'.format( \
                                                            first_param['name'], first, second_param['name'], second)
            with open('{0}/out{1}.txt'.format(output_folder, counter), 'w') as f:
                # Print options in file start
                print(first_param['name'], first, file=f)
                print(second_param['name'], second, '\n', file=f)

                # Print recognition in file
                print(pytesseract.image_to_string(img, lang='rus', config=config), file=f)

            counter += 1


def match_with_ideal():
    files = os.listdir(output_folder)

    text1 = open(ideal_file_path).read().split('\n')
    # text1_set = set(text1)

    lines1 = open(ideal_file_path).readlines()

    for file in files:
        file_path = output_folder + '/' + file

        text2 = open(file_path).read().split('\n')
        # text2_set = set(text2)

        lines2 = open(file_path).readlines()
        #
        # added = text1_set - text2_set
        # removed = text2_set - text1_set
        #
        # for line in text1_set:
        #     if line in added:
        #         print('- ', line.strip())
        #     elif line in removed:
        #         print('+ ', line.strip())
        #
        # for line in text2_set:
        #     if line in added:
        #         print('- ', line.strip())
        #     elif line in removed:
        #         print('+ ', line.strip())
        #
        # print('#' * 60)

        with open('{0}/diff_{1}'.format(output_folder, file), 'w') as f:

            for line in difflib.unified_diff(lines1, lines2, fromfile='ideal', tofile=file):
                print(line, file=f)

        persetage = difflib.SequenceMatcher(None, text1, text2).ratio() * 100
        print(file, persetage, '%')
        print('#'*40)


if __name__ == '__main__':

    path = r'385299605.tif'

    img = Image.open(path)

    # clear output folder folder
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)



    # [start, stop)
    parameters = [
        {
            'name' : 'tosp_min_sane_kn_sp',
            'start': 9,
            'stop' : 10,
            'step' : 1
        }
    ]

    parameter_with_preset = {
        'parameter': {
            'name' : 'textord_blshift_maxshift',
            'start': 0,
            'stop' : 2,
            'step' : 0.5
        },
        'preset': [
            {
                'name': 'textord_noise_rowratio',
                'value': 4
            },
            {
                'name': 'textord_noise_sxfract',
                'value': 5
            },
            {
                'name': 'textord_initialasc_ile',
                'value': 6
            }
        ]
    }

    # test_one(img, parameters, output_folder)
    # correlation(img, parameters[0], parameters[1])
    # test_one_with_preset(img, parameter_with_preset)
    # match_with_ideal()



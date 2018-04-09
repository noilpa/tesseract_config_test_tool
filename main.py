try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

counter = 0

# change for your tesseract path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'


def test_one(img, parameters):

    global counter

    for parameter in parameters:

        start = parameter['start']
        stop  = parameter['stop']
        step  = parameter['step']
        name  = parameter['name']

        for value in range(start, stop, step):
            config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" -c {0}={1}'.format( \
                name, value)

            with open('out{0}.txt'.format(counter), 'w') as f:

                # Print options in file start
                print(name, value, '\n', file=f)

                # Print recognition in file
                print(pytesseract.image_to_string(img, lang='rus', config=config), file=f)

            counter += 1


def test_one_with_preset(img, parameter_with_preset):

    global counter

    start = parameter_with_preset['parameter']['start']
    stop = parameter_with_preset['parameter']['stop']
    step = parameter_with_preset['parameter']['step']
    name = parameter_with_preset['parameter']['name']

    preset_options = ''

    for item in parameter_with_preset['preset']:
        preset_options = preset_options + str(item['name']) + '=' + str(item['value']) + ' '

    preset_options.strip()

    for value in range(start, stop, step):
        config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" -c {0}={1} {2}'.format( \
            name, value, preset_options)
        with open('out{0}.txt'.format(counter), 'w') as f:
            # Print options in file start
            print(name, value, file=f)
            print(preset_options, '\n', file=f)

            # Print recognition in file
            print(pytesseract.image_to_string(img, lang='rus', config=config), file=f)

        counter += 1


def correlation(img, first_param, second_param):

    global counter

    for first in range(first_param['start'], first_param['stop'], first_param['step']):
        for second in range(second_param['start'], second_param['stop'], second_param['step']):
            config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" -c {0}={1} {2}={3}'.format( \
                                                            first_param['name'], first, second_param['name'], second)
            with open('out{0}.txt'.format(counter), 'w') as f:
                # Print options in file start
                print(first_param['name'], first, file=f)
                print(second_param['name'], second, '\n', file=f)

                # Print recognition in file
                print(pytesseract.image_to_string(img, lang='rus', config=config), file=f)

            counter += 1


if __name__ == '__main__':

    path = r'385299605.tif'

    img = Image.open(path)

    # [start, stop)
    parameters = [
        {
            'name' : 'textord_blshift_maxshift',
            'start': 0,
            'stop' : 2,
            'step' :1
        },
        {
            'name': 'textord_noise_rowratio',
            'start': 0,
            'stop': 2,
            'step': 1
        }
    ]

    parameter_with_preset = {
        'parameter': {
            'name' : 'textord_blshift_maxshift',
            'start': 0,
            'stop' : 2,
            'step' :1
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

    # test_one(img, parameters)
    # correlation(img, parameters[0], parameters[1])
    # test_one_with_preset(img, parameter_with_preset)


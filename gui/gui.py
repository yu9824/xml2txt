import PySimpleGUI as sg
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from xml2txt import *

window_options = dict(
    font = 'Helvetica 18'
)

main = {}
text_size = (18, 1)

key_input = '-INPUTFILES-'
key_output = '-OUTPUTFOLDER-'

main['layout'] = [
    # [sg.Text('xml → txt (diffraction)')],
    [sg.Text('input files (.xml)', size = text_size), sg.Input(key = key_input, enable_events=True), sg.FilesBrowse(file_types=(('PDF-card(xml)', '.xml'),))],
    [sg.Text('output folder', size = text_size), sg.Input(key= key_output), sg.FolderBrowse()],
    [sg.OK(), sg.Cancel()]
]

main['window'] = sg.Window('xml2txt', main['layout'], **window_options, element_justification='center')

while True:
    main['event'], main['values'] = main['window'].read()
    if main['event'] == 'Cancel' or main['event'] is None:
        break
    elif main['event'] == key_input:
        if main['values'][key_output] == '':
            main['window'][key_output].Update(os.path.dirname(main['values'][key_input]))
    else:
        for fpath_input in main['values'][key_input].split(';'):
            # check file
            if os.path.isfile(fpath_input):
                df = xml2df(fpath_input)
            else:
                sg.PopupError('FileNotFound', **window_options)
            
            # create output file path
            fpath_output = os.path.join(main['values'][key_output], os.path.splitext(os.path.basename(fpath_input))[0] + '.txt')
            if os.path.isfile(fpath_output):
                flag_overwrite = sg.popup_yes_no('Overwrite?', **window_options)
            if flag_overwrite == 'Yes':
                df.to_csv(fpath_output, encoding = 'utf_8_sig', index = False)
            else:
                continue
            sg.popup_ok('Finished!', **window_options)
main['window'].close()


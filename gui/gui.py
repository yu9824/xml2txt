import PySimpleGUI as sg
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from xml2txt import *

window_options = {}
window_options['font'] = 'Helvetica 18'

main = {}
text_size = (18, 1)

main['layout'] = [
    # [sg.Text('xml → txt (diffraction)')],
    [sg.Text('input files (.xml)', size = text_size), sg.Input('', key = '-INPUTFILES-'), sg.FilesBrowse(initial_folder = os.path.join(os.environ['HOME'], 'Desktop'))],
    [sg.Text('output folder', size = text_size), sg.Input(os.path.join(os.environ['HOME'], 'Desktop'), key = '-OUTPUTFOLDER-'), sg.FolderBrowse(initial_folder = os.path.join(os.environ['HOME'], 'Desktop'))],
    [sg.OK(), sg.Cancel()]
]

main['window'] = sg.Window('xml2txt', main['layout'], **window_options, element_justification='center')

while True:
    main['event'], main['values'] = main['window'].read()
    if main['event'] == 'Cancel' or main['event'] is None:
        break
    else:
        for file in main['values']['-INPUTFILES-'].split(';'):
            df = xml2df(file)
            outputfilepath = os.path.join(main['values']['-OUTPUTFOLDER-'], os.path.splitext(os.path.basename(file))[0] + 'txt')
            df.to_csv(outputfilepath, encoding = 'utf_8_sig', index = False)
            sg.popup_ok('Finished!', **window_options)
main['window'].close()


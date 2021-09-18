import re
# import matplotlib.pyplot as plt # デバッグ用
import pandas as pd
from decimal import Decimal


def xml2df(fpath, start = 10, end = 60, thres = 0.001):
    # float to Decimal
    thres = Decimal(str(thres))

    with open(fpath, mode = 'r', encoding = 'utf_8') as f:
        content = f.read()#.replace('\n', '')
    intensity = content[content.find('<stick_series'):content.find('</stick_series')]
    # print(re.findall('<intensity>(.*)</intensity>', intensity))

    milli = Decimal('0.001')
    def convert(s):
        less_than = '&lt;'  # '<'
        if less_than in s:  # 1milliより小さいことを意味するはずなので，無視．
            return 0
        if s == 'm':
            return milli
        elif 'm' in s:
            return Decimal(s.replace('m', '')) * milli
        elif s.isdigit():
            return Decimal(s)
        else:
            raise ValueError('Cannot convert {0} integer or float.'.format(s))

    intensities = list(map(convert, re.findall('<intensity>(.*)</intensity>', intensity)))
    thetas = list(map(Decimal, re.findall('<theta>(.*)</theta>', intensity)))
    if len(intensities) != len(thetas):
        raise ValueError('`intensities` and `thetas` do not have same length.')

    forgraph = [[start], [0]]
    for k, theta in enumerate(thetas):
        if theta < start:
            continue
        elif theta < end:
            forgraph[0].append(theta-thres)
            forgraph[1].append(0)
            forgraph[0].append(theta)
            forgraph[1].append(intensities[k])
            forgraph[0].append(theta+thres)
            forgraph[1].append(0)
        else:
            break
    forgraph[0].append(end)
    forgraph[1].append(0)

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(*forgraph)
    # ax.set_xlim(start, end)
    # ax.set_ylim(0, None)

    df = pd.DataFrame(forgraph).T
    df.columns = ['theta', 'intensity']
    return df

if __name__ == '__main__':
    fpath = 'example/PDF Card - 01-082-3446.xml'
    df = xml2df(fpath)
    df.to_csv('example/output.txt', encoding = 'utf_8_sig', index = False)





import re
# import matplotlib.pyplot as plt # デバッグ用
import pandas as pd


def xml2df(file, start = 10, end = 60, thres = 0.001):
    with open(file, mode = 'r', encoding = 'utf_8') as f:
        content = f.read()#.replace('\n', '')
    intensity = content[content.find('<stick_series'):content.find('</stick_series')]
    # print(re.findall('<intensity>(.*)</intensity>', intensity))

    milli = 1 * 10 ** -3
    def convert(s):
        if s == 'm':
            return milli
        elif 'm' in s:
            return int(s.replace('m', '')) * milli
        else:
            return int(s)
    intensities = map(convert, re.findall('<intensity>(.*)</intensity>', intensity))
    thetas = map(float, re.findall('<theta>(.*)</theta>', intensity))
    diff = dict(zip(thetas, intensities))

    forgraph = [[start], [0]]
    for k, theta in enumerate(diff):
        if theta < start:
            continue
        elif theta < end:
            forgraph[0].append(theta-thres)
            forgraph[1].append(0)
            forgraph[0].append(theta)
            forgraph[1].append(diff[theta])
            forgraph[0].append(theta+thres)
            forgraph[1].append(0)
        else:
            forgraph[0].append(end)
            forgraph[1].append(0)
            break
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(*forgraph)
    # ax.set_xlim(start, end)
    # ax.set_ylim(0, None)

    df = pd.DataFrame(forgraph).T
    df.columns = ['theta', 'intensity']
    return df

if __name__ == '__main__':
    file = 'example/PDF Card - 01-082-3446.xml'
    df = xml2df(file)
    df.to_csv('example/output.txt', encoding = 'utf_8_sig', index = False)





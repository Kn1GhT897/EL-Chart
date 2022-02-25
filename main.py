import json
import subprocess as sp
from datetime import datetime

import parser
import spider
from configs import configs
from push import send_alert, send_report


def main():
    if datetime.now().day == 1:
        with open('chart.png', 'rb') as fp:
            image = fp.read()
        send_report('<img src="cid:chart"/>', [(image, '<chart>')])

    records, today = spider.update()
    if today < configs.alert.threshold:
        send_alert(f'截至 {datetime.now().strftime("%m 月 %d 日 %H:%M")}，您的宿舍仅剩 <b>{today}</b> 度电')

    data = {
        'month': datetime.now().strftime('%Y-%m'),
        'data': parser.parse(records)
    }
    json.dump(data, open('charts/data.json', 'w'))
    sp.run('cd charts; node index.js', shell=True)


if __name__ == '__main__':
    main()

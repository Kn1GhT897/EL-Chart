import json
import subprocess as sp
from datetime import datetime
from random import randint

from loguru import logger

import parser
import spider
from configs import configs
from push import send_alert, send_report


def main():
    with open('random', 'w') as fp:
        fp.write(f'{randint(100000, 999999)}')

    if datetime.now().day == 1:
        logger.info('触发每月 1 日自动推送')
        with open('chart.png', 'rb') as fp:
            image = fp.read()
        send_report('<img src="cid:chart"/>', [(image, '<chart>')])

    logger.info('正在查询电费余额')
    records, today = spider.update()
    if records is not None:
        if today < configs.alert.threshold:
            logger.info('正在推送消息...')
            send_alert(f'截至 {datetime.now().strftime("%m 月 %d 日 %H:%M")}，您的宿舍仅剩 <b>{today}</b> 度电')

        data = {
            'month': datetime.now().strftime('%Y-%m'),
            'data': parser.parse(records)
        }
        json.dump(data, open('charts/data.json', 'w'))
        logger.info('正在更新图表...')
        sp.run('cd charts; node index.js', shell=True)


if __name__ == '__main__':
    main()

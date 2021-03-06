import os
import pickle
import re
from datetime import datetime

import httpx
from configs import configs
from loguru import logger


def fetch():
    # noinspection HttpUrlsUsage
    return httpx.get(
        'http://wxpay.hnu.edu.cn/api/appElectricCharge/checkRoomNo',
        params={
            'parkNo': 3,
            'buildingNo': 40,
            'roomNo': 529
        },
        headers={
            'X-Requested-With': 'XMLHttpRequest',
        }
    ).json()


def update():
    record_path = os.path.join(os.path.dirname(__file__), 'records.pck')

    # records: map<date-str, value>
    records = pickle.load(open(record_path, 'rb'))
    new_records = {}

    time_now = datetime.now()
    for date in records:
        if (time_now - datetime.strptime(date, '%Y-%m-%d')).days < 40:
            new_records[date] = records[date]

    today = float(re.search('[0-9.]+', fetch()['data']['Balance']).group())
    today_str = time_now.strftime('%Y-%m-%d')
    if today_str not in new_records:
        new_records[today_str] = today
    elif not configs.alert.always:
        logger.info('今日记录已存在，不再触发推送')
        return None, None

    pickle.dump(new_records, open(record_path, 'wb'))

    return new_records, today

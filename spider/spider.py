import os
import pickle
import re
from datetime import datetime

import httpx


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
    new_records[time_now.strftime('%Y-%m-%d')] = today

    pickle.dump(new_records, open(record_path, 'wb'))

    return new_records, today

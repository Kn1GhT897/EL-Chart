from datetime import datetime, timedelta

date_format = '%Y-%m-%d'


def parse(records):
    data = []
    now = datetime.now()
    today = datetime(year=now.year, month=now.month, day=now.day)
    begin = datetime(year=today.year, month=today.month, day=1)
    while today >= begin:
        today_str = today.strftime(date_format)
        yesterday = today - timedelta(days=1)
        yesterday_str = yesterday.strftime(date_format)
        if yesterday_str not in records:
            records[yesterday_str] = records[today_str]
        delta = round(records[yesterday_str] - records[today_str], 2)
        data.append([
            today.strftime(date_format),
            delta, f'{delta}'
        ])
        today = yesterday
    return data

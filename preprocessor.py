import re
import pandas as pd

def preprocess(data) :
    pattern = r"\d{2}\/\d{2}\/\d{4},\s\d{2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[2:]
    dates = re.findall(pattern, data)[1:]

    df = pd.DataFrame({'Date & time': dates, 'message': messages})
    df['Date & time'] = pd.to_datetime(df['Date & time'], format='%d/%m/%Y, %H:%M - ')

    user = list()
    msg = list()

    for message in df['message']:
        text = re.split(r'([\w\W]+?):\s', message)
        if text[1:]:
            user.append(text[1])
            msg.append(text[2])
        else:
            user.append('group_notification')
            msg.append(text[0])

    df['users'] = user
    df['msg'] = msg

    df['only_date'] = df['Date & time'].dt.date
    df['day_name'] = df['Date & time'].dt.day_name()
    df['year'] = df['Date & time'].dt.year
    df['month'] = df['Date & time'].dt.month_name()
    df['day'] = df['Date & time'].dt.day
    df['hour'] = df['Date & time'].dt.hour
    df['minute'] = df['Date & time'].dt.minute

    df = df.drop(columns=['Date & time', 'message'])

    return df
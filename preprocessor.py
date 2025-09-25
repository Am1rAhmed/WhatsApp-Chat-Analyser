import re
import pandas as pd

# It will Preprocess the data and return the dataframe
def preprocess(data):
    # Message Extracting
    pattern = r'\s-\s'
    message = [re.split(pattern, line)[1] if re.split(pattern, line)[1:] else line for line in data.split('\n')]

    # Date and time Extracting

    if 'AM' in data or 'PM' in data or 'am' in data or 'pm' in data:
        date_pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[apAP][mM]\s-)\s'
        dates = [re.findall(date_pattern, line)[0] if re.findall(date_pattern, line) else '' for line in data.split('\n')]
        if dates[0] == '':
            date_pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-)\s'
            dates = [re.findall(date_pattern, line)[0] if re.findall(date_pattern, line) else '' for line in data.split('\n')]

    for i in range(len(dates)):
        dates[i] = dates[i].replace(' -', '')
        dates[i] = dates[i].replace(' -', '')

    df = pd.DataFrame({'user_message': message, 'message_date': dates})
    
    # Mixed is used to convert the string date format into the date-time format
    df['message_date'] = pd.to_datetime(df['message_date'], format='mixed')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    #separate users and messages
    users = []
    messages = []
    for msg in df['user_message']:
        entry = msg.split(':')
        if entry[1:]: #username
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'],inplace = True)
    df['daily_timeline'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour-1))
    df['period']  = period
    # Taaki mera sirf users aaye dataframe mai chats na aaye 
    df_new = df.dropna()
    return df_new
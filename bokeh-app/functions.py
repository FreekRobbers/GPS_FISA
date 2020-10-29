import datetime

# function converts speed to avg2kTime:
# speed: each sample represents real time speed (m/s)
# to
# avg2kTime: each sample represents average speed so far (2k time)
def speedToAvgTime(speed):
    avg2kTime = []
    try:
        avg2kTime.append(datetime.timedelta(seconds=2000/speed[0]))
    except:
        avg2kTime.append(0)
    for i in range(len(speed)-1):
        try:
            avg2kTime.append(datetime.timedelta(seconds=2000/speed[0:i+1].mean()))
        except:
            avg2kTime.append(0)
    return avg2kTime

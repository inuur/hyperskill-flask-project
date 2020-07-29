import datetime as dt

temp = dt.datetime.utcnow() + dt.timedelta(0, 10800)
time = temp.time()
print(time)

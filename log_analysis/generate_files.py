import datetime

number_of_files = 3

today = datetime.date.today()

for _ in range(365):
    prefix = today.strftime('%Y%m%d')
    for i in range(number_of_files):
        open('{0}_{1}.txt'.format(prefix, i), 'w').write('Hello!')
    today = today.fromordinal(today.toordinal()-1)

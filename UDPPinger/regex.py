import re
from datetime import datetime
from time import sleep

# dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(dateTime)
#
# matchObject = re.search("\d{2}:\d{2}:\d{2}", dateTime)
# print(matchObject)




#############

dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
dateTimeObject = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')

sleep(3)

dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
dateTimeObject2 = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')

timeElapsed = dateTimeObject2 - dateTimeObject
print(timeElapsed)

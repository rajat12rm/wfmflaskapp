from datetime import datetime
print(datetime.now())
print(str(datetime.now()).replace(" ",'-').replace(":",'-').replace(".","-"))
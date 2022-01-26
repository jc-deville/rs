import platform
import csv
import shutil

user = input("RobinHood Username:\n")
pw = input("RobinHood Passwrod:\n")
2fa = input("Do you use 2 Factor Authentication for login? (y/n)\n")

if 2fa == 'y':
    totp = input("Enter you 2FA generation secret \n(This can be found in your authenticator app):\n")
else:
    totp = ''

tick = input("What Crypto do you want to trade?\n")

filename = 'config.csv'
tempfile = NamedTemporaryFile(mode='w',delete=False)

fields = ['user','pass','totp','runSys','tradeActive','accountVal','tradePrice','currQuant','ticker']

with open(filename,'r') as csvfile, tempfile:
    reader = csv.DictReader(csvfile, fieldnames=fields)
    writer = csv.DictWriter(tempfile, fieldnames=fields)
    for row in reader:
        row['user'],row['pass'],row['totp'],row['tick'] = user,pw,totp,tick
    row = {'user':row['user'],'pass':row['pass'],'totp':row['totp'],'ticker':row['tick']}
    writer.writerow(row)

shutil.move(tempfile.name,filename)

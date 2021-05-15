import os, sys, time
hostname = "8.8.8.8"
response = os.system("ping -c 1 " + hostname + " >/dev/null 2>&1")

if response == 0:
      print (hostname, 'Reboot successful!')
      sys.exit(0)
else:
      sys.stderr.write(hostname + ' Rebooting..')

sleep_wait=1
max_ping_wait=10
count=0
while (count < max_ping_wait and os.system("ping -c 1 " + hostname + " >/dev/null 2>&1")):
      sys.stderr.write('.')
      time.sleep(sleep_wait)
      count+=1

if (count < max_ping_wait):
    print (hostname, 'Reboot successful!')
    sys.exit(0)
else:
    print (hostname, 'Reboot unsuccessful.')
    sys.exit(1)

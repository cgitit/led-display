import os
from os import remove
from sys import argv

cmd1 = "echo 'PASSWORD' | sudo -S chown root:root wpa_supplicant.conf"
cmd2 = "echo 'PASSWORD' | sudo -S cp -f /home/pi/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf"
cmd3 = "echo 'PASSWORD' | sudo -S cp -f /home/pi/dhcpcd.conf /etc/dhcpcd.conf"
cmd4 = "echo 'PASSWORD' | sudo -S cp -f /home/pi/hostapd.conf /etc/hostapd/hostapd.conf"
cmd5 = "echo 'PASSWORD' | sudo -S systemctl restart wpa_supplicant"
os.system(cmd1 ; cmd2 ; cmd3 ; cmd4 ; cmd5)
#uncomment below to auto delete this file after it has been run.
#remove(argv[0])

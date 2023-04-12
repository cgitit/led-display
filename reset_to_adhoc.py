import os
from os import remove
from sys import argv

cmd1 = "echo 'PASSWORD' | sudo -S chown pi:pi wpa_supplicant.conf"
cmd2 = "echo 'PASSWORD' | sudo -S cp -f /home/pi/wpa_supplicant2.conf /etc/wpa_supplicant/wpa_supplicant.conf"
cmd3 = "echo 'PASSWORD' | sudo -S cp -f /home/pi/dhcpcd2.conf /etc/dhcpcd.conf"
cmd4 = "echo 'PASSWORD' | sudo -S cp -f /home/pi/hostapd2.conf /etc/hostapd/hostapd.conf"
os.system(cmd1 ; cmd2 ; cmd3 ; cmd4)
#uncomment below to auto delete this file after completion
#remove(argv[0])


#Asssuming 
# user: admin 
# password: admin


#RASPI
#Set up library
sudo apt update
sudo apt install libcamera-apps


#RASPI
#Set up directory (Picture taking and replace the old one like realtime update)
mkdir -p /home/admin/Desktop/test_pic
sudo nano /home/admin/Desktop/test_pic/capture_images.sh


#RASPI
#(Optional) .py code for picture taking by stacking. Included (timestamp, reboot count, continue timestamp of the filename)
sudo nano /home/admin/Desktop/test_pic/video_capture.py
#


#RASPI
#Set up the hotspot 
#file name || setup_hotspot.sh ||


#PC
#Connected SSH with computer


#RASPI
#Start the Python HTTP server on port 8000
cd /home/admin/Desktop/test_pic
#Run 2 files
./capture_image.sh &
python3 -m http.server 8000


#PC Browser
http://192.168.4.1:8000/image.jpg &


#Killing background running 
jobs
#This will show all background jobs with their job IDs (like [1] or [2])
kill %1


#Remove Login requirement
sudo nano /etc/systemd/system/getty@tty1.service.d/autologin.conf
#If the directory doesn't exist, create
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d
#///////////////////////////////////////////////////////////////////
#       [Service]
#       ExecStart=
#       ExecStart=-/sbin/agetty --autologin admin --noclear %I $TERM
#///////////////////////////////////////////////////////////////////
#SAVE AND EXIT
sudo systemctl enable getty@tty1
sudo reboot


#Automatically Run capture_image.sh and http on Boot
sudo nano /home/admin/startup_tasks.sh
#Add the following content
#///////////////////////////////////////////////////////////////////
#!/bin/bash
#       Start the image capture script
#       /home/admin/Desktop/test_pic/capture_image.sh &
#       # Start the HTTP server to serve images
#       python3 -m http.server 8000 --directory /home/admin/Desktop/test_pic &
#///////////////////////////////////////////////////////////////////
#SAVE AND EXIT
chmod +x /home/admin/startup_tasks.sh
sudo nano /etc/systemd/system/startup_tasks.service
#Add the following content
#///////////////////////////////////////////////////////////////////
#       [Unit]
#       Description=Run Capture Script and HTTP Server
#       After=network.target
#
#       [Service]
#       ExecStart=/home/admin/startup_tasks.sh
#       Restart=always
#       User=admin
#       Group=admin
#
#       [Install]
#       WantedBy=multi-user.target
#///////////////////////////////////////////////////////////////////
#SAVE AND EXIT
sudo systemctl enable startup_tasks.service
sudo systemctl start startup_tasks.service
#Recheck
sudo systemctl status startup_tasks.service
sudo reboot


#Automatically Reboot if Something Goes Wrong
sudo nano /etc/systemd/system/capture_image.service
#Add the following content
#///////////////////////////////////////////////////////////////////
#       [Unit]
#       Description=Capture Images with Camera
#       After=network.target

#       [Service]
#       ExecStart=/home/admin/Desktop/test_pic/capture_image.sh
#       Restart=always
#       User=admin
#       Group=admin
#       WorkingDirectory=/home/admin/Desktop/test_pic
#
#       [Install]
#       WantedBy=multi-user.target
#///////////////////////////////////////////////////////////////////
#SAVE AND EXIT
sudo systemctl enable capture_image.service
sudo systemctl start capture_image.service
#Recheck
sudo systemctl status capture_image.service


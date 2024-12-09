#!/bin/bash

# Update and install necessary packages
sudo apt update
sudo apt install -y hostapd dnsmasq dhcpcd5

# Stop services before configuration
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

# Configure hostapd
HOSTAPD_CONF="/etc/hostapd/hostapd.conf"
sudo bash -c "cat > $HOSTAPD_CONF <<EOF
interface=wlan0
driver=nl80211
ssid=MyPiHotspot
hw_mode=g
channel=7
wpa=2
wpa_passphrase=YourSecurePassword
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF"

# Point to the hostapd configuration file
HOSTAPD_DEFAULT="/etc/default/hostapd"
sudo bash -c "cat > $HOSTAPD_DEFAULT <<EOF
DAEMON_CONF=\"$HOSTAPD_CONF\"
EOF"

# Configure dnsmasq
DNSMASQ_CONF="/etc/dnsmasq.conf"
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo bash -c "cat > $DNSMASQ_CONF <<EOF
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,12h
EOF"

# Set up static IP for wlan0
DHCPD_CONF="/etc/dhcpcd.conf"
sudo bash -c "cat >> $DHCPD_CONF <<EOF
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant
EOF"

# Manually assign IP to wlan0
sudo ip addr add 192.168.4.1/24 dev wlan0


# Enable and start services
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
sudo systemctl restart dhcpcd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Optionally reboot the system
read -p "Setup complete. Do you want to reboot now? (y/n): " REBOOT
if [ "$REBOOT" == "y" ]; then
    sudo reboot
fi

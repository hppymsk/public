###########################
## associates-laptops.sh ##
## Written by: dru1d     ##
## 02/26/17              ##
## Revision: 3.0         ##
###########################
# Core Application Install/Laptop Build
# Core applications
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install -y build-essential checkinstall bzip2 nmap sshfs ike-scan openvpn network-manager-openvpn network-manager-openvpn-gnome remmina remmina-common remmina-plugin-gnome remmina-plugin-xdmcp remmina-plugin-vnc remmina-plugin-gnome remmina-plugin-rdp linux-headers-generic laptop-mode-tools libssl-dev dconf-tools git-core stunnel4 inetutils-traceroute make libopenmpi-dev openmpi-bin libssl-dev filezilla curl openconnect network-manager-openconnect network-manager-openconnect-gnome vpnc network-manager-vpnc evolution nfs-common xutils-dev xterm whois samdump2 snmp libapache2-mod-dnssd nfs-kernel-server ant dos2unix finger nbtscan autofs miredo ekiga p7zip-full p7zip-full wireshark

# Perl libraries
sudo apt-get install -y libnetaddr-ip-perl libthread-serialize-perl libwww-perl libhtml-tableextract-perl libevent-rpc-perl libhttp-daemon-ssl-perl libnet-imap-simple-perl libnet-smtp-ssl-perl libnet-ldap-perl libnet-smtps-perl libnet-telnet-perl libstring-crc32-perl libdbi-perl libdbd-sybase-perl libswitch-perl

# Python libraries
sudo apt-get install -y python python-cheetah python-bs4 python-lxml python-html5lib python-qt4-dev  python-couchdbkit python3-netaddr python-pip python3-pip python-distribute python3-dev python3-mysql.connector python-openssl python-lxml python-pyasn1 jython python3-bs4

# Ruby libraries
sudo apt-get install -y ruby2.3 ruby-soap4r ruby-ntlm ruby-rainbow ruby-nokogiri

# I turn this off so I can modify /etc/resolv.conf if necessary
#Stop services
sudo systemctl stop avahi-*
#Remove dnsmasq
sudo apt-get remove dnsmasq
#remove avahi-daemon
sudo apt-get remove avahi-dnsconfd
sudo apt-get remove avahi-daemon
sudo apt-get autoremove -y

#Disable Extraneous Services
echo manual | sudo tee /etc/init/nmbd.override
echo manual | sudo tee /etc/init/smbd.override
echo manual | sudo tee /etc/init/avahi-daemon.override
echo manual | sudo tee /etc/init/avahi-dnsconfd.override

# Ruby Gems
sudo gem install httpclient

# Perl libraries
# sudo cpan reload -> Module does not exist; deprecated command?
sudo cpan Crypt::DES
sudo cpan Crypt::Rijndael
sudo cpan Digest::SHA1
sudo cpan Thread::Pool
sudo cpan HTML::TagParser
sudo cpan URI::Fetch
sudo cpan Net::SSL
sudo cpan Net::SNMP
sudo cpan String::CRC32
sudo cpan Thread::Conveyor
sudo cpan Authen::NTLM

# Rebuild the search database
sudo updatedb

# Clean /boot partition
# Normally wouldn't automate this, but it works well and cleans up any extra kernel images
sudo apt-get autoremove -y
sudo update-grub

# Create /h folders
sudo mkdir /h
sudo mkdir /h/toolbox
sudo mkdir /h/client
sudo mkdir /h/bin
# shared.client is a NFS folder that bismark suggested using on gigs
sudo mkdir /h/shared.client
# Change ownership of local files to 
sudo chown -R $(whoami):$(whoami) /h

#add user to wireshark group
sudo usermod -a -G wireshark $(whoami)

#force reboot
sudo reboot
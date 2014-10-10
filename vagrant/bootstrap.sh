#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

locale-gen en_GB.UTF-8

echo ""
echo "### Fixing dns entries"
sed -i -e"s/domain-name-servers, //g" /etc/dhcp/dhclient.conf
if [ -z "`grep -Fl 'prepend domain-name-servers 8.8.8.8,8.8.4.4;' /etc/dhcp/dhclient.conf`" ]; then
    echo $'\n'"prepend domain-name-servers 8.8.8.8,8.8.4.4;" >> /etc/dhcp/dhclient.conf
fi
(dhclient -r && dhclient eth0)

ntpdate ntp.ubuntu.com

echo ""
echo "### Add color prompt"
touch /home/vagrant/.nano_history
chown vagrant:vagrant /home/vagrant/.nano_history
sed -i -e"s/#force_color_prompt=yes/force_color_prompt=yes/g" /home/vagrant/.bashrc
source /home/vagrant/.bashrc

echo ""
echo "### Updating apt data"
apt-get update

echo "### Installing necessary packages"
apt-get -q -y install \
    htop build-essential git git-flow nodejs npm \
    mysql-server-5.5 mysql-client-5.5 libmysqlclient-dev \
    apache2 php5 php5-mysql \
    pyton-dev python-pip

echo ""
echo "### Cleanup packages"
apt-get -q -y autoremove

PHP_SETTINGS='	display_errors = On
 	error_reporting = E_ALL'
echo "${PHP_SETTINGS}" > /etc/php5/apache2/conf.d/90-local.project.ini

service apache2 restart

echo ""
echo "### Install pip requirements"
sudo pip install -r /var/www/pyAPI/pyapi/requirements.txt

# sudo apt-get install phpmyadmin
# uncomment $cfg['Servers'][$i]['AllowNoPassword'] = TRUE;


echo ""
echo "### Bootstrap completed"

exit 0

Setting up Raspberry Pi Sensor
==========

1. Execute `setup.sh` script to setup virtual environment.
2. Install required system packages
3. Setup permissions to user `tshark`
4. Download and install `aircrack-ng`

### 1 - Execute `setup.sh`
Must have `virtualenv` installed
```bash
./setup.sh
```

### 2 - Install required packages
```bash
sudo apt-get install git python-dev python-virtualenv libxml2-dev libxslt-dev \
    libssl-dev tshark
```

### 3 - Enable permissions for current user to use `tshark`
If running the sensor as someone different than ${USER} you must run these
commands for it also.
```bash
sudo chgrp ${USER} /usr/bin/dumpcap
sudo chmod 750 /usr/bin/dumpcap
sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/dumpcap
```

### 4 - Download and Install aircrack
http://blog.petrilopia.net/linux/raspberry-pi-install-aircrackng-suite
```bash
wget http://download.aircrack-ng.org/aircrack-ng-1.2-beta1.tar.gz
tar -zxvf aircrack-ng-1.2-beta1.tar.gz
cd aircrack-ng-1.2-beta1
make
sudo make install
sudo airodump-ng-oui-update
rm -r aircrack-ng-1.2-beta1
rm aircrack-ng-1.2-beta1.tar.gz
```

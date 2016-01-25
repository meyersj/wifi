Setting up Raspberry Pi Sensor
==============================

## Running

```bash
# after following Setup steps
sudo ./bin/start_monitoring.sh
./env/bin/python runner.py
```
`bin/wifimonitor_init` contains an `init.d` daemon script used to run the sensor as a service.
The `dir` and `user` variables will muse be set to match your system.

Once configured, copy file to `/etc/init.d`
```bash
sudo cp ./bin/wifimonitor_init /etc/init.d/wifimon

# start the server
sudo service wifimon start
```

## Setup

#### 1. Execute `setup.sh` script to setup virtual environment.

Must have Python's `virtualenv` installed
```bash
./setup.sh
```
After running, open up `conf/config.py` and set the parameters to correct values.

#### 2. Install required system packages
```bash
sudo apt-get install git python-dev python-virtualenv libxml2-dev libxslt-dev \
    libssl-dev tshark
```

#### 3. Setup permissions for using `tshark`
If running the sensor as someone different than `${USER}` you must run these
commands for it also.
```bash
sudo chgrp ${USER} /usr/bin/dumpcap
sudo chmod 750 /usr/bin/dumpcap
sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/dumpcap
```

#### 4. Download and install `aircrack-ng`
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

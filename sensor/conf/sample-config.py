interface = "mon0"                              # required
sensor_mac = "0.0.0.0"                          # required
sensor = "sensor1"                              # optional
location = "location1"                          # optional
endpoint = "<endpoint for packets>"             # optional


interval= 30    # how often a payload is sent over the network
timeout= 295    # total time to listen for packets
unique = 5      # minimum time interval (seconds) for distinct (sub, sa, ta, da, ra)

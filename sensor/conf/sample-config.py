interface = "mon0"                          # interface from airmon-ng      required
sensor_mac = "XX:XX:XX:XX:XX:XX"            # mac address of wifi card      [optional]
sensor = "default"                          # name of sensor                [optional]
location = "default"                        # name of location              [optional]
endpoint = "http://127.0.0.1:8005/packet"   # endpoint to receive packets   required
payload_timer = 5                           # seconds between requests
distinct_timer = 15                         # time between distinct (src, dst) packets 

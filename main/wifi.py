import time
import subprocess


class WIFI(object):
    def __init__(self):
        self.ret = None
        self.wifi = False

    def wifi_y_n(self):
        self.ret = subprocess.call("ping baidu.com -n 1", creationflags=0x08000000)
        if self.ret == 0:
            self.wifi = True
        else:
            self.wifi = False

    def wifi_update_time(self, sleep):
        while True:
            self.wifi_y_n()
            if self.wifi:
                break
            time.sleep(sleep)


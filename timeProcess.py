class myTime:
    def __init__(self, time_str):
        self.str2attri(time_str)

    def str2attri(self, time_str):
        """
        将字符串形式的时间转化为属性，时间可能有以下几种形式：
        1. xx时xx分xx秒
        2. xx分xx秒
        3. xx秒
        """
        if '时' in time_str:
            self.hour = int(time_str.split('时')[0])
            time_str = time_str.split('时')[1]
        else:
            self.hour = 0
        if '分' in time_str:
            self.minute = int(time_str.split('分')[0])
            time_str = time_str.split('分')[1]
        else:
            self.minute = 0
        if '秒' in time_str:
            self.second = int(time_str.split('秒')[0])
        else:
            self.second = 0


    def get_minute(self):
        return int(self.hour * 60 + self.minute + self.second / 60)
    
    def get_second(self):
        return self.hour * 3600 + self.minute * 60 + self.second
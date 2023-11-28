# 从account.txt中读取账号密码

class Account:
    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

def get_account():
    account = Account()
    with open("./account.txt", "r") as f:
        account.username = f.readline().strip()
        account.password = f.readline().strip()
    return account

if __name__ == "__main__":
    account = get_account()
    print(account.username)
    print(account.password)
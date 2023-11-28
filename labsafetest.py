import time
import requests
from threading import Timer
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from account import get_account
from imgMatch import match
from timeProcess import myTime

driver_path = "./msedgedriver.exe"
op = Options()
op.add_argument('log-level=3')  # 隐藏日志
s = Service(executable_path=driver_path)
driver = webdriver.Edge(service=s, options=op)

account = get_account()

WAIT = WebDriverWait(driver, 10)  # 等待器
driver.get("https://labsafetest.uestc.edu.cn/")

element = WAIT.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='button' and @value='统一身份认证登录']")))
element.click()

element = WAIT.until(EC.presence_of_element_located((By.ID, "username")))
element.send_keys(account.username)
element = driver.find_element(By.ID, "password")
element.send_keys(account.password)
element = driver.find_element(By.CLASS_NAME, "auth_login_btn")
element.click()

# 破解滑动验证码
element = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'block')))
# 获取canvas标签的长宽
canvas_width = element.size['width']
# 拿到背景图片，获取img标签的src属性
element = driver.find_element(By.ID, "img1")
img1_url = element.get_attribute("src")
# 截取其中的base64编码
img1_base64 = img1_url.split(",")[1]
# 拿到滑块图片，获取img标签的src属性
element = driver.find_element(By.ID, "img2")
img2_url = element.get_attribute("src")
# 截取其中的base64编码
img2_base64 = img2_url.split(",")[1]

# 计算滑块的位置
x = match(img1_base64, img2_base64, canvas_width)
# 滑动滑块
element = driver.find_element(By.CLASS_NAME, "slider")
action = webdriver.ActionChains(driver)
action.drag_and_drop_by_offset(element, xoffset=x, yoffset=0).perform()

# 获取title为“安全标识”的a标签
element = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, "two")))
element.click()
#
# # 获取学习时长span标签
# time_span = WAIT.until(EC.presence_of_element_located((By.ID, "xuexi_online")))
# print("学习时长：" + time_span.text)

data = {
    "cmd": "xuexi_online",
}
cookies = driver.get_cookies()
cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
headers = {
    "Origin": "https://labsafetest.uestc.edu.cn",
    "Referer": "https://labsafetest.uestc.edu.cn/redir.php?catalog_id=132&object_id=2590",
}
driver.quit()


def sendPost(data, cookies_dict, headers):
    res = requests.post("https://labsafetest.uestc.edu.cn/exam_xuexi_online.php", data=data, cookies=cookies_dict,
                        headers=headers)
    res = res.json()
    print("学习时长：" + res['shichang'])
    return myTime(res['shichang']).hour


def schedule():
    print("")
    res = sendPost(data, cookies_dict, headers)
    if res >= 2:
        print("已完成学习")
        exit(0)
    Timer(60, schedule).start()


schedule()

# 在控制台加一个跳动的光标，表示程序正在运行
while True:
    print(">", end="")
    time.sleep(1)

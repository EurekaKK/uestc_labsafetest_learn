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

# 获取学习时长span标签
time_span = WAIT.until(EC.presence_of_element_located((By.ID, "xuexi_online")))
print("学习时长：" + time_span.text)

WAIT2 = WebDriverWait(driver, 360)  # 等待器
while True:
    if time_span.text[0] >= '2':
        print("学习时长已满足要求")
        break
    # 获取当前页面弹出的alert，要处理异常
    try:
        alert = WAIT2.until(EC.alert_is_present())
        # 点击确定按钮
        alert.accept()
        print("学习时长：" + time_span.text)
    except:
        print("六分钟了还没弹出alert,你电网站做得太烂了,把浏览器放到前台会好点")

driver.quit()
input("按任意键退出")

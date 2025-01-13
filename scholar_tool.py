from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Define the proxy server
# PROXY = "127.0.0.1:7890"
#
# # Set ChromeOptions()
# options = webdriver.ChromeOptions()
#
# # Add the proxy as argument
# options.add_argument("--proxy-server=%s" % PROXY)
# driver = webdriver.Chrome(options=options)

index = 1

# 启动Chromedriver
driver = webdriver.Chrome()

# 获取"cited by"链接页面
cited_by_url = "https://scholar.google.com/scholar?hl=en&as_sdt=2005&sciodt=1%2C5&cites=3683089856994200319&scipsc=1&q=monocular+depth+estimation&btnG="
driver.get(cited_by_url)

# 判断是否出现机器人检测
# print("verify robot check is here.")
# try:
#     WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "robot-check")))  # 根据实际情况修改定位元素的方式和条件
#     print("请手动完成机器人验证...")
#
#     # 等待验证成功后继续执行
#     WebDriverWait(driver, 300, poll_frequency=1).until_not(EC.presence_of_element_located((By.ID, "robot-check")))
#     print("机器人验证成功，继续执行后续代码。")
# except:
#     print("网页已经正常")

current_url = driver.current_url
driver.get(current_url)

paper_with_citednums = []

# 获取所有页面的论文名称
while True:
    print("get paper list")
    paper_names = []
    paper_cited_nums = []

    paper_elements = driver.find_elements(By.XPATH, "//h3[@class='gs_rt']")
    paper_names.extend([element.text for element in paper_elements])

    cited_elem = driver.find_elements(By.XPATH, "//*[contains(text(),'Cited by ')]")
    paper_cited_nums.extend([int(element.text.split()[-1]) for element in cited_elem])

    paper_with_citednums.extend(zip(paper_names, paper_cited_nums))

    # 查找下一页按钮
    try:
        print('click next page')
        next_button = driver.find_element(By.XPATH, "//*[@id=\"gs_n\"]/center/table/tbody/tr/td[12]/a/span")
        next_button.click()
        import random

        random_number = random.uniform(0, 1)
        # print(random_number)
        time.sleep(2 * random_number + 1)  # 等待页面加载
    except:
        break

sorted_by_second = sorted(paper_with_citednums, key=lambda tup: tup[1], reverse=True)

# 将论文名称写入txt文件
with open("paper_names{}.txt".format(index), "w") as file:
    for name in sorted_by_second:
        file.write(str(name[1]) + '\t' + name[0] + "\n")

# 关闭浏览器
driver.quit()

print("paper list已经写入到paper names{}.txt文件中。".format(index))

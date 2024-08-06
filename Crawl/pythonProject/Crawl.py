import time
import random

from openpyxl import Workbook

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

# 设置为开发者模式，防止被各大网站识别出来使用了Selenium console中输入window.navigator.webdriver 测试
def get_browser():
    browser = webdriver.Chrome()
    # 2.使用js关闭检测机制
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
                """
    })

    # 3.返回浏览器对象
    return browser


def page_turning(reslist,page_num):
    print(f'正在跳转至第{page_num}页')
    try:
        # 使用JavaScript滚动到页面底部
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 找到下一页的按钮
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Pagination--pgWrap--kfPsaVv > div > div > button.next-btn.next-medium.next-btn-normal.next-pagination-item.next-next > span')))
        submit.click()
        # 判断页码是否和当前页相等
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Pagination--pgWrap--kfPsaVv > div > div > div > button.next-btn.next-medium.next-btn-normal.next-pagination-item.next-current'), str(page_num)))
        print("跳转页面成功")
        get_products(reslist,page_num)   # 获取该页商品数据
    except TimeoutException:
        page_turning(reslist,page_num)


def simulate_scroll():
    """
    模拟鼠标慢慢滚动以加载商品图片
    :return:
    """
    # 获取页面高度
    page_height = browser.execute_script("return document.body.scrollHeight")

    # 定义滚动步长和间隔时间
    scroll_step = 8  # 每次滚动的距离
    scroll_delay = 2  # 每次滚动的间隔时间（秒）

    # 模拟慢慢滚动
    current_position = 0
    while current_position < page_height:
        # 计算下一个滚动位置
        next_position = current_position + scroll_step

        # 执行滚动动作
        browser.execute_script(f"window.scrollTo(0, {next_position});")

        # 等待一段时间
        browser.implicitly_wait(scroll_delay)

        # 更新当前滚动位置
        current_position = next_position


def get_products(reslist,page_num):
    """
    获取对应页码下的所有商品
    :param page_num:页码
    :return:
    """
    print(f"正在提取第{page_num}页的商品信息...")
    # time.sleep(random.randint(3, 5))
    time.sleep(3)
    simulate_scroll()   # 模拟鼠标慢慢滚动以加载图片
    # time.sleep(random.randint(3, 5))
    time.sleep(3)
    html = browser.page_source
    doc = pq(html)

    # 提取所有商品的共同父元素的类选择器
    items = doc('div.PageContent--contentWrap--mep7AEm > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div').items()
    for item in items:
        title = item.find('.Title--title--jCOPvpf > span').text()   # 定位商品标题
        # image = item.find('.MainPic--mainPicWrapper--iv9Yv90 > img').attr('src')   # 定位商品图片地址
        price = item.find('span.Price--priceInt--ZlsSi_M').text() + item.find('span.Price--priceFloat--h2RR0RK').text()  # 定位价格
        deal = item.find('.Price--realSales--FhTZc7U').text()   # 定位交易量
        shop = item.find('.ShopInfo--shopName--rg6mGmy').text()   # 定位店名

        # 定位所在地信息
        location = item.find('div.Price--priceWrapper--Q0Dn7pN > div:nth-child(4) > span').text() + ' ' + item.find('div.Price--priceWrapper--Q0Dn7pN > div:nth-child(5) > span').text()

        pricenum = 0.0
        if price != '':
            pricenum = float(price)

        product = {
            '价格': pricenum,
            '商品简介': title,
            '交易数量': deal,
            '店铺名称': shop,
            '店铺所在地': location
        }
        if pricenum >= 10:
            reslist.append([product['商品简介'], product['价格'], product['交易数量'], product['店铺名称'], product['店铺所在地']])
        # print("ws LIST : ")

        # print(product)

def search_goods(start_page, total_pages, keyword):
    """
    抓取索引页
    :param page: 页码
    """
    ws = []  # 信息list
    print(f'正在爬取第{start_page}页')
    try:
        url = 'https://s.taobao.com'
        browser.get(url)
        time.sleep(6)  # 强制停止5秒,手动扫码登录

        # 找到搜索输入框
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        # 找到搜索按钮
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_SearchForm > div > div.search-button > button')))

        input_box.send_keys(keyword)
        search_button.click()

        # 搜索商品后会再强制等待10秒，如有滑块请手动操作
        time.sleep(8)

        if start_page != 1:
            # 使用JavaScript滚动到页面底部
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(1, 3))  # 滑倒底部后停留 1 - 3 秒

            # 定位到页面底部的页码输入框
            page_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pageContent"]/div[1]/div[3]/div[4]/div/div/span[3]/input')))
            print('定位到页面底部的页码输入框成功')
            page_box.clear()  # 清空输入框
            page_box.send_keys(start_page)  # 调用 send_keys()方法将页码填充到输入框中

            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pageContent > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Pagination--pgWrap--kfPsaVv > div > div > button.next-btn.next-medium.next-btn-normal.next-pagination-jump-go > span')))
            submit.click()

        # 获取每一页的信息
        get_products(ws,start_page)

        for i in range(start_page + 1, start_page + total_pages):
            page_turning(ws,i)
        # wb.save(r'淘宝商品数据.xlsx')
        return sorted(ws,key=lambda x:x[1],reverse=True)

    except TimeoutException as e:
        print("搜索商品超时", e)
        search_goods(start_page, total_pages)


browser = get_browser()
wait = WebDriverWait(browser, 30)
# if __name__ == '__main__':


def crawl(page_start = 1, page_all = 1, keyword='瓦罗兰特马来服代充'):
    try:
        # browser = get_browser()
        # wait = WebDriverWait(browser, 30)

        # wb = Workbook()   # 新建工作簿
        # ws = wb.active    # 获取工作表

        # ws.append(['商品简介', '价格', '交易数量', '店铺名称', '店铺所在地', '商品图片'])
        print("pagenum: %d" % page_all)
        return search_goods(page_start, page_all,keyword)

    except Exception as e:
        print("main函数报错:", e)

# res = crawl(1,3)
# print(crawl(1,3))
# with open('data.txt', 'w') as file:
#     # 写入列表1
#     file.write('List 1:\n')
#     for item in res:
#         file.write(str(item) + '\n')  # 将数值转换为字符串并写入
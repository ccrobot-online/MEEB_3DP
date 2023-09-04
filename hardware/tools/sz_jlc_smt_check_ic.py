#!/usr/bin/env python
# coding: utf-8

# ## 嘉立创的SMT库存查询

# In[9]:

from selenium.webdriver.common.action_chains import ActionChains
import time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
import json
import time
from datetime import datetime
import logging

from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from termcolor import colored
from pytz import timezone
from removebg import RemoveBg

import pytest  # 增加单元测试


def move_to_gap(driver, slider, headless=True):  # slider是要移动的滑块,tracks是要传入的移动轨迹
    actions = ActionChains(driver)
    print(driver)
    print(slider)
    print(actions)

    if headless:
        actions.move_to_element(slider)
        actions.click_and_hold(slider)
    else:
        # actions.move_to_element(slider).perform()
        # actions.click_and_hold(slider).perform()
        actions.move_to_element(slider)
        actions.click_and_hold(slider)

    ActionChains(driver).move_by_offset(xoffset=2, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=98, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=100, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=100, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=100, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=30, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=10, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=3, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
    time.sleep(1)
    ActionChains(driver).release().perform()


def login_off(browser):
    browser.close()  # 关闭页面
    browser.quit()  # 关闭整个浏览器


def login_jlc(id, pw, headless=True):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920x1080")  # 指定浏览器分辨率

    if headless:
        chrome_options.add_argument("--headless")
    else:
        pass

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("disable-infobars")

    # options = Options()
    # options.binary_location = "d:/cv5/TC/totalcmd_v9.12/TOOL_cv/Chrome-bin/chrome.exe"
    # driver_path=r'd:\cv5\TC\totalcmd_v9.12\TOOL_cv\chromedriver\chromedriver.exe'
    # browser = webdriver.Chrome(chrome_options=options, executable_path=driver_path, options=chrome_options)

    if True == headless:
        browser = webdriver.Chrome(options=chrome_options)
    else:
        options = Options()
        options.binary_location = (
            "d:/cv5/TC/totalcmd_v9.12/TOOL_cv/Chrome-bin/chrome.exe"
        )
        driver_path = r"d:\cv5\TC\totalcmd_v9.12\TOOL_cv\chromedriver\chromedriver.exe"
        browser = webdriver.Chrome(
            chrome_options=options, executable_path=driver_path, options=chrome_options
        )

    browser.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
        },
    )
    browser.execute_cdp_cmd("Network.enable", {})
    browser.execute_cdp_cmd(
        "Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}}
    )

    browser.get("https://www.jlc.com/")

    locator = (By.LINK_TEXT, "用户登录")
    WebDriverWait(browser, 100, 1).until(EC.presence_of_element_located(locator))

    browser.find_element_by_xpath(
        '//*[@id="loginSuccessHide"]/div[1]/ul/li[2]/a'
    ).click()

    locator = (By.LINK_TEXT, "忘记密码？")
    WebDriverWait(browser, 100, 1).until(EC.presence_of_element_located(locator))

    browser.find_element_by_xpath(
        '//*[@id="loginSuccessHide"]/div[1]/div/div[2]/div[1]/div[1]/input'
    ).send_keys(id)
    browser.find_element_by_xpath(
        '//*[@id="loginSuccessHide"]/div[1]/div/div[2]/div[1]/div[2]/input'
    ).send_keys(pw)

    try:
        dragger = browser.find_element_by_xpath('//*[@id="nc_2__bg"]')
        print("找到滑块元素")
    except:
        print(colored("没有找到滑块元素", "red"))
        pass
    else:
        move_to_gap(browser, dragger, headless)
    print("滑块移动完成")

    browser.find_element_by_xpath(
        '//*[@id="loginSuccessHide"]/div[1]/div/div[2]/div[1]/div[4]/button[1]'
    ).click()

    locator = (By.LINK_TEXT, "进入下单平台")
    WebDriverWait(browser, 60 * 3, 1).until(EC.presence_of_element_located(locator))
    print(browser.find_element_by_link_text("进入下单平台").get_attribute("href"))

    browser.find_element_by_xpath('//*[@id="login"]').click()

    # 关闭弹出的最新信息
    browser.find_element_by_xpath('//*[@id="onile_message_div"]/div/div[1]/a').click()

    return browser


def open_part_page(browser):
    # 转到主页面
    goto_main_frame(browser)

    # 等页面成功打开
    locator = (By.PARTIAL_LINK_TEXT, "可贴片元器件列表")
    WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))

    # 打开SMT器件查询页面
    browser.find_element_by_xpath('//*[@id="smt_ul_id"]/li[4]/a').click()
    print("smt page bingo!!!")

    # 转到查询IC的frame
    WebDriverWait(browser, 60, 1).until(
        EC.frame_to_be_available_and_switch_to_it(
            browser.find_element_by_name("client_context_frame")
        )
    )
    print("frame bingo!!!")


def open_pcb_page(browser):
    # 转到主页面
    goto_main_frame(browser)

    # 等页面成功打开
    locator = (By.PARTIAL_LINK_TEXT, "PCB订单列表")
    WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))

    # 打开PCB订单查询页面
    browser.find_element_by_xpath('//*[@id="newPcbOrderIndexList"]').click()
    print("pcb order page bingo!!!")

    # 转到查询的frame
    WebDriverWait(browser, 60, 1).until(
        EC.frame_to_be_available_and_switch_to_it(
            browser.find_element_by_name("client_context_frame")
        )
    )
    print("frame bingo!!!")


def open_smt_page(browser):
    # 转到主页面
    goto_main_frame(browser)

    # 等页面成功打开
    locator = (By.PARTIAL_LINK_TEXT, "SMT订单列表")
    WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))

    # 打开SMT订单查询页面
    browser.find_element_by_xpath('//*[@id="smt_ul_id"]/li[2]/a').click()
    print(colored("SMT order page bingo!!!", "green"))

    # 转到查询的frame
    WebDriverWait(browser, 60, 1).until(
        EC.frame_to_be_available_and_switch_to_it(
            browser.find_element_by_name("client_context_frame")
        )
    )
    print(colored("frame bingo!!!", "green"))


def goto_main_frame(browser):
    browser.switch_to.default_content()


def get_smt_order_info(browser, order_id):
    ###
    ###
    dict = {}
    # 等页面成功打开
    locator = (
        By.XPATH,
        '//*[@id="defiendScrollDiv"]/div/table/tbody/tr[2]/td/table/tbody/tr/td[1]/strong',
    )
    WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))
    table = browser.find_element_by_xpath(
        '//*[@id="defiendScrollDiv"]/div/table/tbody/tr[3]/td/div[1]/table'
    )  # 找到这个table

    time.sleep(5)  # 等网页加载

    table_tr_list = table.find_elements_by_css_selector("tr")

    for tr in table_tr_list:
        if tr.get_attribute("class") == "rowSelectStyle":  # 找到行
            table_td_list = tr.find_elements_by_css_selector("td")
            for td in table_td_list:
                if td.get_attribute("class") == "ztjj":  # 找到列
                    table_a_list = td.find_elements_by_css_selector("a")
                    for a in table_a_list:
                        if a.text.strip() == order_id:  # 找到定单
                            print(
                                colored("find **{}**", "green").format(td.text.strip())
                            )
                            table_td_list[9].click()
                            time.sleep(3)
                            break
                    else:
                        continue
                    break
            else:
                continue
            break

    now_handle = browser.current_window_handle
    print(now_handle)
    all_handles = browser.window_handles
    print(all_handles)

    for handle in all_handles:
        if handle != now_handle:
            # 输出待选择的窗口句柄
            print(handle)
            browser.switch_to.window(handle)

            print("以下为新弹出界面信息")
            print(browser.current_url)
            print(browser.title)

            if browser.title.strip() == "自助平台-查看SMT可制造性设计检查结果":
                # 获取信息
                board_img = browser.find_element_by_xpath(
                    '//*[@id="pageObject"]/div/div[6]/img'
                )
                dict["board_img"] = board_img.get_attribute("src")
                browser.get(dict["board_img"])  # 只能在登陆状态下下载文件

                dfm = "dfm_screenshot.png"
                if dfm in os.listdir():
                    pass
                else:
                    browser.save_screenshot(dfm)
                    rmbg = RemoveBg("7T2XUxbtVQhiGJLN2LfshL18", "error.log")
                    rmbg.remove_background_from_img_file(dfm)

                # 关闭当前窗口
                browser.close()

    # 输出主窗口句柄
    browser.switch_to.window(now_handle)

    return dict


def get_pcb_order_info(browser, order_id, utc=False):
    ###
    ###
    dict = {}
    # 等页面成功打开
    locator = (By.XPATH, '//*[@id="myAngularBox"]/div[1]/div[2]')
    WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))
    info = browser.find_element_by_xpath('//*[@id="myAngularBox"]/div[1]/div[2]')

    if utc:
        # 2020-03-03 03:23:11
        fmt = "%Y-%m-%d %H:%M:%S"
        order_time = datetime.strptime(order_id, fmt)
        order_time = order_time.astimezone(tzinfo=timezone("Asia/Shanghai"))
        order_id = order_time.strftime(fmt)
        print(colored("order id use china time is: {}".format(order_id), "green"))
    else:
        pass

    div_number = 0
    ii = 0
    while div_number < 150:
        ii += 1
        time.sleep(1)
        info_list = info.find_elements_by_css_selector("div")
        div_number = len(info_list)
        print("本页一共有div: {}个".format(len(info_list)))

        if 120 <= ii:
            break

    find_it = False
    for inf in info_list:
        if inf.get_attribute("class") == "tableListBox mt16 ng-scope":  # 找到匹配的行
            newlist = inf.find_elements_by_css_selector("div")
            print("本行一共有div: {}个".format(len(newlist)))
            for inf2 in newlist:
                if inf2.get_attribute("class") == "pull-left ml8 over color6":
                    newlist2 = inf2.find_elements_by_css_selector("p")
                    for inf3 in newlist2:
                        if (
                            inf3.get_attribute("class")
                            == "pull-left ml25 line28 ng-binding"
                        ):
                            print(inf3.text)
                            if inf3.text.strip() == order_id:
                                # find the order
                                print("find the order, and now break!!!!!!")
                                find_it = True
                                break
                    else:
                        continue
                    break

            if find_it:
                # add the pic of the board to dict, 还没实现
                for inf2 in newlist:
                    if inf2.get_attribute("class") == "pull-left":
                        # img = inf2.find_element_by_tag_name('img')
                        img = inf2.find_element_by_css_selector("img")
                        print(img.get_attribute("src"), inf2)
                        # browser.get(img.get_attribute('src'))      #只能在登陆状态下下载文件
                        # browser.save_screenshot("screenshot_.png")
                        # img.click()

            if find_it:
                for inf2 in newlist:
                    if inf2.get_attribute("class") == "tableAlign textleft":
                        span_list = inf2.find_elements_by_css_selector("span")
                        for span in span_list:
                            if len(span.find_elements_by_css_selector("i")) != 0:
                                # print(inf.text)
                                span.click()
                                break
                        else:
                            continue
                        break
                else:
                    continue
                break
            else:
                print(colored("本行row没有找到订单，换下一行！", "red"))
    ####################
    # 等页面成功打开
    locator = (
        By.XPATH,
        '//*[@id="pcbOrderDetailModal"]/div/div/div/div[2]/div/div/div[2]/div/div[1]/h4/label[2]',
    )
    WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))

    board_num = browser.find_element_by_xpath(
        '//*[@id="pcbOrderDetailModal"]/div/div/div/div[2]/div/div/div[2]/div/table[1]/tbody/tr[2]/td[4]'
    )

    print(board_num.text)

    pcb_all_price = browser.find_element_by_xpath(
        '//*[@id="pcbOrderDetailModal"]/div/div/div/div[2]/div/div/div[2]/div/div[3]/div[1]/p'
    )

    print(pcb_all_price.text)

    smt_all_price = browser.find_element_by_xpath(
        '//*[@id="pcbOrderDetailModal"]/div/div/div/div[2]/div/div/div[2]/div/div[3]/div[2]/p'
    )

    print(smt_all_price.text)

    smt_order_id = browser.find_element_by_xpath(
        '//*[@id="pcbOrderDetailModal"]/div/div/div/div[2]/div/div/div[2]/div/div[1]/h4/label[2]'
    )
    print(smt_order_id.text)

    # 关闭弹出的具体信息
    # browser.find_element_by_xpath('//*[@id="pcbOrderDetailModal"]/div/div/div/div[1]/button').click()

    dict["num"] = int(board_num.text)
    dict["pcb_price"] = float(pcb_all_price.text.split(":")[1].strip("元").strip())
    dict["smt_price"] = float(smt_all_price.text.split(":")[1].strip("元").strip())
    dict["smt_order_id"] = smt_order_id.text.split("：")[1].strip()

    return dict


def get_part_info(browser, ic_id, headless=True):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    dict = {}

    locator = (By.XPATH, '//*[@id="queryKeywordText"]')
    WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))
    WebDriverWait(browser, 60, 1).until(EC.element_to_be_clickable(locator)).click()
    browser.find_element_by_xpath('//*[@id="queryKeywordText"]').clear()
    browser.find_element_by_xpath('//*[@id="queryKeywordText"]').click()
    browser.find_element_by_xpath('//*[@id="queryKeywordText"]').send_keys(ic_id)

    locator = (By.XPATH, '//*[@id="search_button"]')
    WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))
    WebDriverWait(browser, 60, 1).until(EC.element_to_be_clickable(locator)).click()

    locator = (By.LINK_TEXT, ic_id)

    try:
        WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))
    except Exception as e:
        print(colored("No No No {} is found!!!".format(ic_id), "red"))
        return dict

    table = browser.find_element_by_xpath(
        '//*[@id="defiendScrollDiv"]/div[2]/table[2]/tbody/tr/td/div[1]/table/tbody'
    )

    table_tr_list = table.find_elements(By.TAG_NAME, "tr")
    # print(len(table_tr_list))

    for tr in table_tr_list:
        table_td_list = tr.find_elements(By.TAG_NAME, "td")
        # print(len(table_td_list))
        for td in table_td_list:
            table_a_list = td.find_elements(By.TAG_NAME, "a")
            if len(table_a_list) > 0:
                if ic_id == td.text.strip():
                    print("find **{}**".format(td.text))
                    print("stocks is **{}**".format(table_td_list[6].text))
                    dict["number"] = int(table_td_list[6].text.strip())
                    dict["type"] = table_td_list[0].text.strip()  # 基础库或者扩展库或者已下架
                    dict["supplier"] = table_td_list[5].text.strip()  # 是否可以预订货存

    print(
        "href is: {}".format(
            browser.find_element_by_link_text(ic_id).get_attribute("href")
        )
    )
    browser.find_element_by_link_text(ic_id).click()

    try:
        locator = (By.LINK_TEXT, "下载")
        WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))
        print(browser.find_element_by_link_text("下载").get_attribute("href"))
    except Exception as e:
        logger.error(str(e), exc_info=True)
        print(colored("error get link!!", "red"))

        locator = (By.LINK_TEXT, "查看元件信息变更记录")
        WebDriverWait(browser, 60, 1).until(EC.presence_of_element_located(locator))
        print(browser.find_element_by_link_text("查看元件信息变更记录").get_attribute("href"))
    else:
        pass

    part_id = browser.find_element_by_xpath('//*[@id="detailsCode"]').text
    if part_id == ic_id:
        dict["id"] = part_id
        print("the part id is: {0:s}".format(dict["id"]))

        dict["price"] = browser.find_element_by_xpath('//*[@id="prices"]').text.split(
            "\n"
        )
        print("Price list:", *dict["price"], sep="\n- ")

        price_list = []
        for single in dict["price"]:
            if "个以内" in single:
                pass
            else:
                if ":" in single:
                    price_list.append(float(single.split(":")[1].strip().strip("￥")))
                else:
                    price_list.append(float(single.split("：")[1].strip().strip("￥")))

        dict["price_max"] = max(price_list)
        dict["price_min"] = min(price_list)

        try:
            dict["download"] = browser.find_element_by_link_text("下载").get_attribute(
                "href"
            )
        except Exception as e:
            logger.error(str(e), exc_info=True)
            print(colored("error get link!!", "red"))

            dict["download"] = ""
        else:
            pass

        dict["pic_url"] = browser.find_element_by_xpath(
            '//*[@id="xzoom-default"]'
        ).get_attribute("src")

        if headless:
            dict["info"] = [
                "headless",
            ]
        else:
            try:
                browser.find_element_by_link_text("查看元件信息变更记录").click()
                # 等待加载完成
                locator = (By.XPATH, '//*[@id="change_componentCode"]')
                print("info: {}".format(locator))
                WebDriverWait(browser, 60, 1).until(
                    EC.presence_of_element_located(locator)
                )

                time.sleep(5)

                info = browser.find_element_by_xpath(
                    '//*[@id="component_change_details"]'
                )

                # print('info: {} {}'.format(info, info.text))
                info_list = info.find_elements_by_css_selector("div")
                # print(len(info_list))

                info_li = []
                for inf in info_list:
                    # print(inf.text)
                    info_li.append(inf.text)

                locator = (
                    By.XPATH,
                    '//*[@id="component_change_record_div"]/div[1]/table/tbody/tr/td[2]/a',
                )
                WebDriverWait(browser, 60 * 5, 1).until(
                    EC.presence_of_element_located(locator)
                ).click()
            except:
                dict["info"] = []
                print(colored("info list read error!!!!!!", "red"))
            else:
                dict["info"] = info_li

    else:
        dict = None

    return dict


if __name__ == "__main__":
    pytest.main()

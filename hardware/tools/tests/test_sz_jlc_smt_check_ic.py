#!/usr/bin/env python
# coding: utf-8
from sz_jlc_smt_check_ic import *
import os
import logging


def test_0():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    os.environ["CV_JLC_ID"] = "18500190963"
    os.environ["CV_JLC_PW"] = "WDN777"

    id = os.environ["CV_JLC_ID"]
    pw = os.environ["CV_JLC_PW"]

    browser = login_jlc(id, pw, headless=False)

    i = 0
    while i < 10:
        i += 1
        time.sleep(5)
        try:
            open_part_page(browser)
            x = get_part_info(browser, "C17168", headless=True)
            print(x)
            x = get_part_info(browser, "C17168", headless=True)
            print(x)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            print(colored("error get part info!!!try again!!! - {}".format(i), "red"))
            continue
        else:
            break

    i = 0
    while i < 10:
        i += 1
        time.sleep(5)
        try:
            open_pcb_page(browser)
            # xx = get_pcb_order_info(browser, '2020-03-20 11:47:40')#样板的订单，使用美国的时间
            xx = get_pcb_order_info(browser, "2020-03-20 19:47:40")  # 样板的订单，使用中国的时间
            print(xx)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            print(
                colored("error get pcb order info!!!try again!!! - {}".format(i), "red")
            )
            continue
        else:
            break

    i = 0
    while i < 10:
        i += 1
        time.sleep(5)
        try:
            open_smt_page(browser)
            xxx = get_smt_order_info(browser, xx["smt_order_id"])
            print(xxx)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            print(
                colored("error get smt order info!!!try again!!! - {}".format(i), "red")
            )
            continue
        else:
            break

    login_off(browser)

#!/usr/bin/env python
# coding: utf-8

# ## 查元件价格及库存

# In[26]:


from requests_html import HTMLSession
import requests
import time

import pytest  # 增加单元测试

# In[35]:


def get_part_info(ic_id):
    session = HTMLSession()
    url = "https://so.szlcsc.com/global.html?k={0:s}".format(ic_id)
    r = session.get(url)
    content = r.html.find("#shop-list", first=True)
    table_list = content.find("table")
    result = []
    for table in table_list:
        list_string = table.text.split("\n")
        ####print(list_string)
        sku = ""
        name = ""
        price_100 = 0
        stock = 0
        # print('\n')
        dict = {}
        price_flag = False
        ####print(len(list_string))
        for i in range(len(list_string)):
            ####print(i)
            if "商品编号" in list_string[i]:
                key, value = list_string[i].split("：", 1)
                value = value.upper().strip()
                dict[key] = value
                # print(dict)
                sku = list_string[i].split("：")[1].upper().strip()
                #######print(sku)
                if sku != ic_id.upper():
                    break

            if "型号" in list_string[i]:
                key, value = list_string[i].split("：", 1)
                value = value.upper().strip()
                dict[key] = value
                # print(dict)
                name = list_string[i].split("：")[1].strip()
                # print(name)

            if price_flag == False:
                if "100+" in list_string[i]:
                    price_100 = float(list_string[i + 1].split(" ")[0].strip("￥"))
                    dict["price_100"] = price_100
                    # print(dict)
                    # print(price_100)
                    price_flag = True
                elif "200+" in list_string[i]:
                    price_100 = float(list_string[i + 1].split(" ")[0].strip("￥"))
                    dict["price_100"] = price_100
                    price_flag = True
                elif "500+" in list_string[i]:
                    price_100 = float(list_string[i + 1].split(" ")[0].strip("￥"))
                    dict["price_100"] = price_100
                    price_flag = True
                elif "1000+" in list_string[i]:
                    price_100 = float(list_string[i + 1].split(" ")[0].strip("￥"))
                    dict["price_100"] = price_100
                    price_flag = True
                elif "10+" in list_string[i]:
                    price_100 = float(list_string[i + 1].split(" ")[0].strip("￥"))
                    dict["price_100"] = price_100
                    price_flag = True
                elif "停售" in list_string[i]:
                    dict["price_100"] = "0"
                    dict["库存"] = "-1"
                    price_flag = True
                    print("已停售")
                    # print("已停售")
                    # print("已停售")

            if "库存：" in list_string[i]:
                stock = int(list_string[i].split("：")[1].strip().split(" ")[0])
                # print(stock)
                key, value = list_string[i].split("：", 1)
                # print(key, value)
                dict[key] = stock
                # print(dict)
            elif "库存充足" in list_string[i]:
                dict["库存"] = "5000"
            elif "库存紧张" in list_string[i]:
                dict["库存"] = "100"
            elif ("到货通知" or "我要订货" or "暂无库存") in list_string[i]:
                dict["库存"] = "0"
                print("暂无库存")
                # print("暂无库存")
                # print("暂无库存")

            ####print(dict)

        if sku == ic_id.upper():
            break

    if sku == ic_id.upper():
        return dict
    else:
        return None


def get_part_price(ic_id, num):
    part = get_part_info(ic_id)
    print(part)
    single_price = float(part["price_100"])
    return single_price * num


if __name__ == "__main__":
    pytest.main()

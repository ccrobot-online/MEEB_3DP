#!/usr/bin/env python
# coding: utf-8

# ## 查元件价格及库存
import os
import xlsxwriter
from datetime import datetime
from pytz import timezone
from termcolor import colored
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

from szlcsc_check_ic import get_part_info as get_lcsc  # 从立创商城获得零件信息
from sz_jlc_smt_check_ic import get_part_info as get_jlc  # 从嘉立创获得零件信息
from sz_jlc_smt_check_ic import login_jlc  # 登陆嘉立创
from sz_jlc_smt_check_ic import login_off  # 登出嘉立创
from sz_jlc_smt_check_ic import open_part_page  # 打开可贴器件页面
from sz_jlc_smt_check_ic import get_pcb_order_info
from sz_jlc_smt_check_ic import *
from dingding import *  # dingding的库
from sent_Adafruit_IO import send_price_to_ada_io


def main():

    fmt = "%Y%m%d_%H%M%S_%Z%z"
    now_utc = datetime.now(timezone("{0:s}/{1:s}".format("Asia", "Shanghai")))
    str_temp = now_utc.strftime(fmt)

    key = os.environ["CV_DINGDING_TOKEN"]

    md = """
## 数据来源

- [MEEB_3DP项目](https://github.com/ccccmagicboy/MEEB_3DP)
- [立创商城抓取](https://www.szlcsc.com/)
- [深圳嘉立创抓取](https://www.sz-jlc.com/)
## 启动时间
"""
    md += "\n" + str_temp

    # ding_ac_single('BOM生成开始', md, 'https://github.com/ccccmagicboy/MEEB_3DP/actions?query=workflow%3A%22CI+-+MEEB_3DP%22', key)

    bom_file_path = os.path.join(
        os.getcwd(), "..", "src", "BOM_MEEB_3DP_ccSCH_038.csv",
    )
    print("Open the BOM file: {0:s}".format(bom_file_path))
    sum_lcsc = 0
    total = 0

    id = os.environ["CV_JLC_ID"]
    pw = os.environ["CV_JLC_PW"]

    browser = login_jlc(id, pw)
    # browser = login_jlc(id, pw, headless = False)

    i = 0
    while i < 10:
        i += 1
        part_list = []  # 从bom读出的raw数据
        part_list_ordered = []  # 经过排序的零件列表
        not_support_smt_jlc = []  # 不支持JLC SMT的零件
        not_install = []  # BOM上不安装的元件
        stop_selling_lcsc = []  # 立创商城停售的
        not_enough_lcsc = []  # 立创商城库存不足的元件
        removed_jlc = []  # 嘉立创下架的元件
        not_enough_jlc = []  # 嘉立创库存不足的元件
        use_ext = []  # 嘉立创扩展库
        time.sleep(3)
        try:
            open_part_page(browser)

            with open(bom_file_path, "r", encoding="utf-16-le") as ff:
                for line in ff.readlines():
                    if "ID\tName\tDesignator\tFootprint\tQuantity" not in line:
                        # print(line)
                        part = line.strip("\n").replace('"', "").split("\t")
                        part_id = part[8]  # 零件的立创ID(Cxxxx)
                        num_needed = int(part[4])  # 单板元件数量
                        # print('{0:s} need {1:d}'.format(part_id, num_needed))
                        part_info = get_lcsc(part_id)
                        print(part_info)

                        single_price = float(part_info["price_100"])
                        stocks_numbers = int(part_info["库存"])
                        # part.append('')#[10] #是否安装
                        part.append(single_price)  # [11]
                        part.append(stocks_numbers)  # [12]

                        if "NO" == part[10]:  # 遇到不安装的件
                            del part[0]
                            part_list.append(part)
                            continue

                        total = single_price * num_needed
                        sum_lcsc += total

                        if "Yes" == part[9]:  # 支持SMT的元件
                            x = get_jlc(browser, part_id)
                            print(x)
                            if x != {}:
                                part.append(x["price_max"])  # 13 float
                                part.append(x["price_min"])  # 14 float
                                part.append(x["number"])  # 15 int
                                part.append(x["info"])  # 16 list
                                part.append(x["pic_url"])  # 17 url string
                                part.append(x["type"])  # 18 smt type
                                part[7] = x["supplier"]  # 7 是否可以预订货存
                            else:
                                part.append(0)  # 13 float
                                part.append(0)  # 14 float
                                part.append(-1)  # 15 int
                                part.append([])  # 16 list
                                part.append("")  # 17 pic url string
                                part.append("已下架")  # 18 smt type

                        del part[0]
                        part_list.append(part)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            print(colored("error get part info!!!try again!!! - {}".format(i), "red"))
            continue
        else:
            break

    print(colored("Size of list is {}".format(len(part_list)), "green"))
    if len(part_list) != 62:
        print(
            colored(
                "Size of list is {}, which is not correct!!!now exit the main.".format(
                    len(part_list)
                ),
                "red",
            )
        )
        return

    i = 0
    while i < 10:
        i += 1
        time.sleep(10)
        try:
            open_pcb_page(browser)
            time.sleep(5)
            smt0 = get_pcb_order_info(browser, "2020-04-29 08:24:37")  # 样板的订单，使用美国的时间
            # smt0 = get_pcb_order_info(browser, '2020-04-29 16:24:37')#样板的订单，使用中国的时间
            print(smt0)

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
        time.sleep(10)
        try:
            open_smt_page(browser)
            xxx = get_smt_order_info(browser, smt0["smt_order_id"])
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

    # 按Designator排序
    part_list.sort(key=lambda part_list: part_list[1])
    i = 0

    # 输出最终的列表
    for part in part_list:
        i += 1
        part = [i,] + part
        print(part)
        part_list_ordered.append(part)

    print("\n")
    # print the no support jlc smt part
    print("Now below are the parts which not support smt mounting by JLC: \n")
    for part in part_list_ordered:
        if part[9] != "Yes":
            print(part)
            not_support_smt_jlc.append(part)

    print("\n")
    # print the no mount parts
    print("Now below are the parts which not install from factory: \n")
    for part in part_list_ordered:
        if part[10] == "NO":
            print(part)
            not_install.append(part)

    print("\n")
    # print the parts 停售的
    print("Now below are the parts NOT SELL ANYMORE from LCSC: \n")
    for part in part_list_ordered:
        if part[12] < 0:
            print(part)
            stop_selling_lcsc.append(part)

    print("\n")
    # print the parts 立创商城库存不足的
    print("Now below are the parts 库存不足 from LCSC: \n")
    for part in part_list_ordered:
        if part[12] <= 100 and part[12] >= 0:
            print(part)
            not_enough_lcsc.append(part)

    # removed_jlc
    print("\n")
    # print the parts JLC下架的
    print("Now below are the parts 下架的 from JLC: \n")
    for part in part_list_ordered:
        if "NO" != part[10] and "Yes" == part[9]:
            if part[15] < 0:
                print(part)
                removed_jlc.append(part)

    print(
        colored(
            "###add 下架的 to both not_support_smt_jlc and not_enough_jlc.###\n", "red"
        )
    )
    for part in removed_jlc:
        not_support_smt_jlc.append(part)
        not_enough_jlc.append(part)

    # not_enough_jlc
    print("\n")
    # print the parts JLC库存不足的
    print("Now below are the parts 库存不足 from JLC: \n")
    for part in part_list_ordered:
        if "NO" != part[10] and "Yes" == part[9]:
            if part[15] <= 100 and part[15] >= 0:
                print(part)
                not_enough_jlc.append(part)

    # use_ext
    print("\n")
    # print the parts 使用扩展库的
    print("Now below are the parts 使用扩展库的 from JLC: \n")
    for part in part_list_ordered:
        if "NO" != part[10] and "Yes" == part[9] and "扩展库" == part[18]:
            print(part)
            use_ext.append(part)

    # 准备输出XLSX文件
    bom_file_path2 = os.path.join(
        os.getcwd(), "..", "bom", "BOM_MEEB_3DP_ccSCH_038.xlsx",
    )

    if os.path.exists(bom_file_path2):
        os.remove(bom_file_path2)

    workbook = xlsxwriter.Workbook(bom_file_path2)

    # 创建主工作表
    worksheet = workbook.add_worksheet("BOM")

    worksheet.repeat_rows(0)  # 第一行重复出现
    worksheet.protect()  # 保护本表

    # 以下是标题的格式
    header_format = workbook.add_format(
        {"border": 1, "text_wrap": True, "locked": True, "font_size": 13, "bold": True,}
    )

    header_format.set_align("left")
    header_format.set_align("vcenter")

    # 以下是普通单元格的格式
    cell_format = workbook.add_format(
        {"border": 1, "text_wrap": True, "locked": True, "font_size": 12,}
    )

    cell_format.set_align("left")
    cell_format.set_align("vcenter")

    # 以下是不安装元件的格式
    cell_format_not_install = workbook.add_format(
        {
            "border": 1,
            "bold": True,
            "font_color": "white",
            "text_wrap": True,
            "locked": True,
            "bg_color": "black",
            "diag_type": 3,
            "diag_border": 7,
            "diag_color": "white",
            "font_size": 12,
        }
    )
    cell_format_not_install.set_align("left")  # 靠左对齐
    cell_format_not_install.set_align("vcenter")  # 居中显示

    # 以下是不SMT零件的格式
    cell_format_not_smt = workbook.add_format(
        {
            "border": 1,
            "bold": True,
            "font_color": "white",
            "text_wrap": True,
            "locked": True,
            "bg_color": "red",
            "font_size": 12,
        }
    )
    cell_format_not_smt.set_align("left")
    cell_format_not_smt.set_align("vcenter")

    # cell_format_not_enouth_jlc 以下是嘉立创库存不足的零件
    cell_format_not_enouth_jlc = workbook.add_format(
        {
            "border": 1,
            "bold": True,
            "font_color": "black",
            "text_wrap": True,
            "locked": True,
            "bg_color": "yellow",
            "font_size": 12,
        }
    )
    cell_format_not_enouth_jlc.set_align("left")
    cell_format_not_enouth_jlc.set_align("vcenter")

    # cell_format_removed_jlc 以下是嘉立创下架的零件
    cell_format_removed_jlc = workbook.add_format(
        {
            "border": 1,
            "bold": True,
            "font_color": "black",
            "text_wrap": True,
            "locked": True,
            "bg_color": "pink",
            "font_size": 12,
        }
    )
    cell_format_removed_jlc.set_align("left")
    cell_format_removed_jlc.set_align("vcenter")

    # 写bom.xlsx
    # 先写标题
    worksheet.write_row(
        0,
        0,
        [
            "ID",
            "Name",
            "Designator",
            "Footprint",
            "Quantity",
            "Manufacturer Part",
            "Manufacturer",
            "Supplier",
            "Supplier Part",
            "LCSC Assembly",
            "安装",
            "立创单价",
            "立创库存",
            "嘉立创单价1",
            "嘉立创单价2",
            "嘉立创库存",
        ],
        header_format,
    )
    # 设置列宽
    worksheet.set_column("A:A", 4)
    worksheet.set_column("B:B", 24)
    worksheet.set_column("C:C", 33)
    worksheet.set_column("D:D", 33)
    worksheet.set_column("E:E", 12)
    worksheet.set_column("F:F", 23)
    worksheet.set_column("G:G", 17)
    worksheet.set_column("H:H", 12)
    worksheet.set_column("I:I", 13)
    worksheet.set_column("J:J", 12)
    worksheet.set_column("L:L", 16)
    worksheet.set_column("M:M", 18)
    # 设置标题行高
    worksheet.set_row(0, 40)

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet.set_landscape()
    worksheet.set_paper(9)  # A4
    worksheet.fit_to_pages(1, 0)
    worksheet.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet.set_footer("&CPage &P of &N")

    i = 0

    for i in range(len(part_list_ordered)):
        xx_str = ""
        worksheet.set_row(i + 1, 40)  # 设置行高
        if part_list_ordered[i][10] == "NO":  # 不安装的列
            worksheet.write_row(
                i + 1, 0, part_list_ordered[i][:16], cell_format_not_install
            )
            worksheet.write_url(
                "I{0:d}".format(i + 2),
                "https://so.szlcsc.com/global.html?k={0:s}".format(
                    part_list_ordered[i][8]
                ),
                cell_format_not_install,
                string="{0:s}".format(part_list_ordered[i][8]),
            )
        elif part_list_ordered[i][9] != "Yes":  # 不SMT的列
            worksheet.write_row(
                i + 1, 0, part_list_ordered[i][:16], cell_format_not_smt
            )
            worksheet.write_url(
                "I{0:d}".format(i + 2),
                "https://so.szlcsc.com/global.html?k={0:s}".format(
                    part_list_ordered[i][8]
                ),
                cell_format_not_smt,
                string="{0:s}".format(part_list_ordered[i][8]),
            )
        else:
            if (
                part_list_ordered[i][15] <= 100 and part_list_ordered[i][15] >= 0
            ):  # 嘉立创SMT库存小于100个大于0个的
                worksheet.write_row(
                    i + 1, 0, part_list_ordered[i][:16], cell_format_not_enouth_jlc
                )
                worksheet.write_url(
                    "I{0:d}".format(i + 2),
                    "https://so.szlcsc.com/global.html?k={0:s}".format(
                        part_list_ordered[i][8]
                    ),
                    cell_format_not_enouth_jlc,
                    string="{0:s}".format(part_list_ordered[i][8]),
                )

                for xx in part_list_ordered[i][16]:
                    xx_str += "\n" + xx
                # https://xlsxwriter.readthedocs.io/working_with_cell_comments.html#cell-comments
                worksheet.write_comment(
                    "J{0:d}".format(i + 2), xx_str, {"x_scale": 2, "y_scale": 10}
                )
                worksheet.write_comment(
                    "I{0:d}".format(i + 2), part_list_ordered[i][18]
                )
            elif part_list_ordered[i][15] < 0:
                worksheet.write_row(
                    i + 1, 0, part_list_ordered[i][:16], cell_format_removed_jlc
                )
                worksheet.write_url(
                    "I{0:d}".format(i + 2),
                    "https://so.szlcsc.com/global.html?k={0:s}".format(
                        part_list_ordered[i][8]
                    ),
                    cell_format_removed_jlc,
                    string="{0:s}".format(part_list_ordered[i][8]),
                )

                for xx in part_list_ordered[i][16]:
                    xx_str += "\n" + xx
                # https://xlsxwriter.readthedocs.io/working_with_cell_comments.html#cell-comments
                worksheet.write_comment(
                    "J{0:d}".format(i + 2), xx_str, {"x_scale": 2, "y_scale": 10}
                )
                worksheet.write_comment(
                    "I{0:d}".format(i + 2), part_list_ordered[i][18]
                )
            else:
                worksheet.write_row(i + 1, 0, part_list_ordered[i][:16], cell_format)
                worksheet.write_url(
                    "I{0:d}".format(i + 2),
                    "https://so.szlcsc.com/global.html?k={0:s}".format(
                        part_list_ordered[i][8]
                    ),
                    cell_format,
                    string="{0:s}".format(part_list_ordered[i][8]),
                )

                for xx in part_list_ordered[i][16]:
                    xx_str += "\n" + xx

                worksheet.write_comment(
                    "J{0:d}".format(i + 2), xx_str, {"x_scale": 2, "y_scale": 10}
                )
                worksheet.write_comment(
                    "I{0:d}".format(i + 2), part_list_ordered[i][18]
                )

    # 总价格计算
    smt0_single_board_price = (smt0["pcb_price"] + smt0["smt_price"]) / smt0["num"]

    smt0_total = 0
    smt0_total2 = 0
    for item in not_support_smt_jlc:
        smt0_total = int(item[4]) * item[11]
        smt0_total2 += smt0_total

    smt0_single_board_price += smt0_total2

    worksheet1 = workbook.add_worksheet("总价格")
    worksheet1.write_row(0, 0, ["ID", "生产计划", "数量", "单价（含税）", "总成本"], header_format)
    worksheet1.write_row(
        1,
        0,
        [
            "1",
            "BOM_力创商城",
            100,
            "{0:.3f}".format(sum_lcsc),
            "{0:.3f}".format(sum_lcsc * 100),
        ],
        cell_format,
    )
    worksheet1.write_row(
        2,
        0,
        [
            "2",
            smt0["smt_order_id"],
            "{0:d}".format(smt0["num"]),
            "{0:.3f}".format(smt0_single_board_price),
            "{0:.3f}".format(smt0["num"] * smt0_single_board_price),
        ],
        cell_format,
    )

    worksheet1.set_column("A:A", 5)
    worksheet1.set_column("B:B", 25)
    worksheet1.set_column("C:C", 40)
    worksheet1.set_column("D:D", 40)
    worksheet1.set_column("E:E", 40)
    worksheet1.set_column("F:F", 23)
    worksheet1.set_column("G:G", 10)
    worksheet1.set_column("H:H", 10)
    worksheet1.set_column("I:I", 10)
    worksheet1.set_column("J:J", 5)
    worksheet1.set_column("L:L", 10)
    worksheet1.set_column("M:M", 10)

    # 设置标题行高
    worksheet1.set_row(0, 40)
    worksheet1.set_row(1, 40)  # 设置行高
    worksheet1.set_row(2, 40)  # 设置行高

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet1.set_landscape()
    worksheet1.set_paper(9)  # A4
    worksheet1.fit_to_pages(1, 0)
    worksheet1.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet1.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-总价页-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet1.set_footer("&CPage &P of &N")
    ###############################################################
    worksheet2 = workbook.add_worksheet("不安装的")
    worksheet2.write_row(
        0,
        0,
        [
            "ID",
            "Name",
            "Designator",
            "Footprint",
            "Quantity",
            "Manufacturer Part",
            "Manufacturer",
            "Supplier",
            "Supplier Part",
            "LCSC Assembly",
            "安装",
            "立创单价",
            "立创库存",
            "嘉立创单价1",
            "嘉立创单价2",
            "嘉立创库存",
        ],
        header_format,
    )
    for i in range(len(not_install)):
        worksheet2.set_row(i + 1, 40)  # 设置行高
        worksheet2.write_row(i + 1, 0, not_install[i][:16], cell_format)
    worksheet2.set_column("A:A", 4)
    worksheet2.set_column("B:B", 24)
    worksheet2.set_column("C:C", 33)
    worksheet2.set_column("D:D", 33)
    worksheet2.set_column("E:E", 6)
    worksheet2.set_column("F:F", 23)
    worksheet2.set_column("G:G", 10)
    worksheet2.set_column("H:H", 10)
    worksheet2.set_column("I:I", 10)
    worksheet2.set_column("J:J", 5)
    worksheet2.set_column("L:L", 10)
    worksheet2.set_column("M:M", 10)
    # 设置标题行高
    worksheet2.set_row(0, 40)

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet2.set_landscape()
    worksheet2.set_paper(9)  # A4
    worksheet2.fit_to_pages(1, 0)
    worksheet2.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet2.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-不安装页-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet2.set_footer("&CPage &P of &N")
    ###############################################################

    worksheet3 = workbook.add_worksheet("嘉立创不能SMT的")
    worksheet3.write_row(
        0,
        0,
        [
            "ID",
            "Name",
            "Designator",
            "Footprint",
            "Quantity",
            "Manufacturer Part",
            "Manufacturer",
            "Supplier",
            "Supplier Part",
            "LCSC Assembly",
            "安装",
            "立创单价",
            "立创库存",
        ],
        header_format,
    )
    for i in range(len(not_support_smt_jlc)):
        worksheet3.set_row(i + 1, 40)  # 设置行高
        worksheet3.write_row(i + 1, 0, not_support_smt_jlc[i][:16], cell_format)

    worksheet3.set_column("A:A", 4)
    worksheet3.set_column("B:B", 24)
    worksheet3.set_column("C:C", 33)
    worksheet3.set_column("D:D", 33)
    worksheet3.set_column("E:E", 6)
    worksheet3.set_column("F:F", 23)
    worksheet3.set_column("G:G", 10)
    worksheet3.set_column("H:H", 10)
    worksheet3.set_column("I:I", 10)
    worksheet3.set_column("J:J", 5)
    worksheet3.set_column("L:L", 10)
    worksheet3.set_column("M:M", 10)
    # 设置标题行高
    worksheet3.set_row(0, 40)

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet3.set_landscape()
    worksheet3.set_paper(9)  # A4
    worksheet3.fit_to_pages(1, 0)
    worksheet3.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet3.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-不能SMT的页-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet3.set_footer("&CPage &P of &N")
    ###############################################################

    worksheet4 = workbook.add_worksheet("立创商城停售的")
    worksheet4.write_row(
        0,
        0,
        [
            "ID",
            "Name",
            "Designator",
            "Footprint",
            "Quantity",
            "Manufacturer Part",
            "Manufacturer",
            "Supplier",
            "Supplier Part",
            "LCSC Assembly",
            "安装",
            "立创单价",
            "立创库存",
            "嘉立创单价1",
            "嘉立创单价2",
            "嘉立创库存",
        ],
        header_format,
    )
    for i in range(len(stop_selling_lcsc)):
        worksheet4.set_row(i + 1, 40)  # 设置行高
        worksheet4.write_row(i + 1, 0, stop_selling_lcsc[i][:16], cell_format)

    worksheet4.set_column("A:A", 4)
    worksheet4.set_column("B:B", 24)
    worksheet4.set_column("C:C", 33)
    worksheet4.set_column("D:D", 33)
    worksheet4.set_column("E:E", 6)
    worksheet4.set_column("F:F", 23)
    worksheet4.set_column("G:G", 10)
    worksheet4.set_column("H:H", 10)
    worksheet4.set_column("I:I", 10)
    worksheet4.set_column("J:J", 5)
    worksheet4.set_column("L:L", 10)
    worksheet4.set_column("M:M", 10)
    # 设置标题行高
    worksheet4.set_row(0, 40)

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet4.set_landscape()
    worksheet4.set_paper(9)  # A4
    worksheet4.fit_to_pages(1, 0)
    worksheet4.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet4.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-立创商城停售的页-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet4.set_footer("&CPage &P of &N")
    ###############################################################

    worksheet5 = workbook.add_worksheet("立创商城库存不足的")
    worksheet5.write_row(
        0,
        0,
        [
            "ID",
            "Name",
            "Designator",
            "Footprint",
            "Quantity",
            "Manufacturer Part",
            "Manufacturer",
            "Supplier",
            "Supplier Part",
            "LCSC Assembly",
            "安装",
            "立创单价",
            "立创库存",
            "嘉立创单价1",
            "嘉立创单价2",
            "嘉立创库存",
        ],
        header_format,
    )
    for i in range(len(not_enough_lcsc)):
        worksheet5.set_row(i + 1, 40)  # 设置行高
        worksheet5.write_row(i + 1, 0, not_enough_lcsc[i][:16], cell_format)

    worksheet5.set_column("A:A", 4)
    worksheet5.set_column("B:B", 24)
    worksheet5.set_column("C:C", 33)
    worksheet5.set_column("D:D", 33)
    worksheet5.set_column("E:E", 6)
    worksheet5.set_column("F:F", 23)
    worksheet5.set_column("G:G", 10)
    worksheet5.set_column("H:H", 10)
    worksheet5.set_column("I:I", 10)
    worksheet5.set_column("J:J", 5)
    worksheet5.set_column("L:L", 10)
    worksheet5.set_column("M:M", 10)
    # 设置标题行高
    worksheet5.set_row(0, 40)

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet5.set_landscape()
    worksheet5.set_paper(9)  # A4
    worksheet5.fit_to_pages(1, 0)
    worksheet5.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet5.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-立创商城库存不足的页-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet5.set_footer("&CPage &P of &N")
    ###############################################################

    worksheet6 = workbook.add_worksheet("JLC库存不足的")
    worksheet6.write_row(
        0,
        0,
        [
            "ID",
            "Name",
            "Designator",
            "Footprint",
            "Quantity",
            "Manufacturer Part",
            "Manufacturer",
            "Supplier",
            "Supplier Part",
            "LCSC Assembly",
            "安装",
            "立创单价",
            "立创库存",
            "嘉立创单价1",
            "嘉立创单价2",
            "嘉立创库存",
        ],
        header_format,
    )
    for i in range(len(not_enough_jlc)):
        worksheet6.set_row(i + 1, 40)  # 设置行高
        worksheet6.write_row(i + 1, 0, not_enough_jlc[i][:16], cell_format)

    worksheet6.set_column("A:A", 4)
    worksheet6.set_column("B:B", 24)
    worksheet6.set_column("C:C", 33)
    worksheet6.set_column("D:D", 33)
    worksheet6.set_column("E:E", 6)
    worksheet6.set_column("F:F", 23)
    worksheet6.set_column("G:G", 10)
    worksheet6.set_column("H:H", 10)
    worksheet6.set_column("I:I", 10)
    worksheet6.set_column("J:J", 5)
    worksheet6.set_column("L:L", 10)
    worksheet6.set_column("M:M", 10)
    # 设置标题行高
    worksheet6.set_row(0, 40)

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet6.set_landscape()
    worksheet6.set_paper(9)  # A4
    worksheet6.fit_to_pages(1, 0)
    worksheet6.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet6.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-SMT库存不足的页-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet6.set_footer("&CPage &P of &N")
    ###############################################################

    worksheet7 = workbook.add_worksheet("被JLC下架的")
    worksheet7.write_row(
        0,
        0,
        [
            "ID",
            "Name",
            "Designator",
            "Footprint",
            "Quantity",
            "Manufacturer Part",
            "Manufacturer",
            "Supplier",
            "Supplier Part",
            "LCSC Assembly",
            "安装",
            "立创单价",
            "立创库存",
            "嘉立创单价1",
            "嘉立创单价2",
            "嘉立创库存",
        ],
        header_format,
    )
    for i in range(len(removed_jlc)):
        worksheet7.set_row(i + 1, 40)  # 设置行高
        worksheet7.write_row(i + 1, 0, removed_jlc[i][:16], cell_format)

    worksheet7.set_column("A:A", 4)
    worksheet7.set_column("B:B", 24)
    worksheet7.set_column("C:C", 33)
    worksheet7.set_column("D:D", 33)
    worksheet7.set_column("E:E", 6)
    worksheet7.set_column("F:F", 23)
    worksheet7.set_column("G:G", 10)
    worksheet7.set_column("H:H", 10)
    worksheet7.set_column("I:I", 10)
    worksheet7.set_column("J:J", 5)
    worksheet7.set_column("L:L", 10)
    worksheet7.set_column("M:M", 10)
    # 设置标题行高
    worksheet7.set_row(0, 40)

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet7.set_landscape()
    worksheet7.set_paper(9)  # A4
    worksheet7.fit_to_pages(1, 0)
    worksheet7.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet7.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-被SMT下架的页-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet7.set_footer("&CPage &P of &N")
    #####################################################################################
    worksheet8 = workbook.add_worksheet("使用JLC扩展库的")
    worksheet8.write_row(
        0,
        0,
        [
            "ID",
            "Name",
            "Designator",
            "Footprint",
            "Quantity",
            "Manufacturer Part",
            "Manufacturer",
            "Supplier",
            "Supplier Part",
            "LCSC Assembly",
            "安装",
            "立创单价",
            "立创库存",
            "嘉立创单价1",
            "嘉立创单价2",
            "嘉立创库存",
        ],
        header_format,
    )
    for i in range(len(use_ext)):
        worksheet8.set_row(i + 1, 40)  # 设置行高
        worksheet8.write_row(i + 1, 0, use_ext[i][:16], cell_format)

    worksheet8.set_column("A:A", 4)
    worksheet8.set_column("B:B", 24)
    worksheet8.set_column("C:C", 33)
    worksheet8.set_column("D:D", 33)
    worksheet8.set_column("E:E", 6)
    worksheet8.set_column("F:F", 23)
    worksheet8.set_column("G:G", 10)
    worksheet8.set_column("H:H", 10)
    worksheet8.set_column("I:I", 10)
    worksheet8.set_column("J:J", 5)
    worksheet8.set_column("L:L", 10)
    worksheet8.set_column("M:M", 10)
    # 设置标题行高
    worksheet8.set_row(0, 40)

    # 设置打印的格式
    # https://xlsxwriter.readthedocs.io/page_setup.html
    worksheet8.set_landscape()
    worksheet8.set_paper(9)  # A4
    worksheet8.fit_to_pages(1, 0)
    worksheet8.set_margins(left=0.3, right=0.3, top=0.75, bottom=0.75)

    command = 'git describe --tags --always --dirty="-dev"'
    temp_str = os.popen(command).read()

    # 设置页眉
    worksheet8.set_header(
        "&L&[Picture]&C&15ccrobot-online.com-MEEB_3DP-使用JLC扩展库的-{0:s}-{1:s}&R&[Picture]".format(
            temp_str, str_temp
        ),
        {"image_left": "logo.jpg", "image_right": "logo.jpg"},
    )
    # 设置页脚
    worksheet8.set_footer("&CPage &P of &N")
    #####################################################################################
    # 关闭文件
    workbook.close()

    # print price
    print("THIS BOM IS COST {0:.3f} RMB（含税） PCS.".format(sum_lcsc), "r")

    command = "echo ::set-output name=price::{0:.3f}".format(sum_lcsc)
    # print(command)
    print(os.popen(command).read())

    ###############################################################

    links = []

    item = {"title": "", "messageURL": "", "picURL": ""}

    item["title"] = temp_str + "MEEB_3DP:{0:.3f} RMB".format(sum_lcsc)
    item[
        "messageURL"
    ] = "https://github.com/ccccmagicboy/MEEB_3DP/actions?query=workflow%3A%22CI+-+MEEB_3DP%22"
    item[
        "picURL"
    ] = "https://raw.githubusercontent.com/ccrobot-online/MEEB_3DP/master/img/meeb_3dp_top.jpg"
    links.append(dict(item))

    for i in range(len(not_enough_jlc)):
        item["title"] = "{0}: {1}".format(not_enough_jlc[i][8], not_enough_jlc[i][15])
        item["messageURL"] = not_enough_jlc[i][17]
        item["picURL"] = not_enough_jlc[i][17]
        links.append(dict(item))

    ding_fc(links, key)

    ###############################################################
    user = os.environ["ADAFRUIT_IO_USERNAME"]
    key2 = os.environ["ADAFRUIT_IO_KEY"]

    send_price_to_ada_io(user, key2, "meeb-3dp-p", sum_lcsc)


if __name__ == "__main__":
    # execute only if run as a script
    # os.environ["DEBUSSY"] = "1"
    os.environ["CV_JLC_ID"] = "18500190963"
    os.environ["CV_JLC_PW"] = "WDNRedghyio90jreweggseegQW189mn"
    os.environ[
        "CV_DINGDING_TOKEN"
    ] = "SEC149c65bfef0df7069427b7972730a3c4ed151871eb4d2b74e4ba38bf0aec5c0f"

    os.environ["ADAFRUIT_IO_USERNAME"] = "cccc"
    os.environ["ADAFRUIT_IO_KEY"] = "f9fc56ca88b348119a65a7063c4d1355"

    main()

#!/usr/bin/env python
# coding: utf-8
from szlcsc_check_ic import *


def test_0():
    part = get_part_info("C22797")
    assert part["商品编号"] == "C22797"
    print(part)


def test_1():
    print(get_part_price("C22797", 10))


def test_2():

    test_list = [
        "C32346",
        "C57156",
        "C488349",
        "C25744",
        "C77321",
        "C70377",
        "C129508",
        "C36191",
        "C114583",
        "C8963",
        "C47647",
        "C192585",
        "C7440",
        "C72047",
        "C24112",
        "C400705",
        "C376619",
        "C17168",
        "C1525",
        "C83291",
        "C76872",
        "C53865",
        "C1555",
        "C142526",
    ]

    for item in test_list:
        part = get_part_info(item)
        assert part["商品编号"] == item
        print(part)

#!/usr/bin/env python

import svgwrite
import svgwrite.utils as svgutils
import re

import xml.dom.minidom

"""Module docstring
"""

fgDefault = "#000000"  # black
bgDefault = "#ffffff"  # white

#:Dictionary of style tuples, one can change it to generate own colors
#:
#:Any style contains tuple in form (background, foreground), both in SVG
#:color form (e.g. ``"#ffffff"`` for ``white``).
# 背景色, 前景色
STYLES = {
    "default": (bgDefault, fgDefault),
    "arduino": ("#c4a000", fgDefault),
    "serial": ("#008c23", "#ffffff"),
    "interr": ("#d3d7cf", fgDefault),
    "timer": ("#ad7fa8", fgDefault),
    "analog": ("#73d216", fgDefault),
    "system": ("#fce94f", fgDefault),
    "power": ("#f40000", bgDefault),
    "ground": (fgDefault, bgDefault),
    "pwm": ("#f57900", fgDefault),
    "neopixel": ("url(#neo_grad)", "white"),
    "nc": ("#666666", "#fffff2"),
    "eth": ("#2626ff", "#fffff2"),
    "sd": ("purple", "white"),
    "dio": ("#ed14fb", "#fffff2"),
    "di": ("#fdbf2d", "#000000"),
    "gpio": ("#ff6600", "#fffff2"),
}

#:List of tuples '(regular expression, style name)'
#:
#:It is used to map pin's function to appropriate color style
# Be free to change it for own needs
STYLLING = [
    ("~?(RESET|XTAL|CLKI|CLKO|CKOUT|dW)", "system"),
    ("~?(ADC|AREF|AIN)", "analog"),
    ("~?(TOSC|T\d|ICP)", "timer"),
    ("~?(PWM)", "pwm"),
    ("VCC|AVCC|VBUS", "power"),
    ("GND", "ground"),
    ("~?(MISO|MOSI|\S?SCK|SS|SCL|SDA|RX|TX)", "serial"),
    ("^DI$", "di"),
    ("^DIO", "dio"),
    ("GPIO", "gpio"),
    ("\d+", "arduino"),
    ("~?(PC)?INT", "interr"),
    ("NEOPIXEL", "neopixel"),
    ("NC", "nc"),
    ("~?(RMII|MD)", "eth"),
    ("~?(SDIO)", "sd"),
]


class header(svgwrite.Drawing):
    pnSize = 20  # pin编号的字体大小
    pfSpace = 12  # 上下间隔
    pfWidth = 150  # 标签的长度
    pfSize = 18  # 标签的高度

    border = 50  # 图的边框，上下左右

    def __init__(self, header_name, pinout=None, pincount=8, nameSize=28):
        self.name = header_name
        self.cnSize = nameSize

        self._pinout = []
        if isinstance(pinout, list):
            self.pinout = pinout
            self.pincount = len(pinout)
        else:
            self.pincount = pincount

        # calculate image size
        imgWidth = (
            self._getLlen(self.pinout) * (self.pfWidth + self.pfSpace)
            + self._getRlen(self.pinout) * (self.pfWidth + self.pfSpace)
            + self._getBodyXsize()
            + self.border * 2
        )
        imgHeight = self._getBodyYsize() + self.border * 2

        super(header, self).__init__(
            filename=header_name + ".svg",
            profile="tiny",
            size=(imgWidth, imgHeight),
            font_family="Exo",
        )

    @property
    def pinout(self):
        """Property of type list
        """
        return self._pinout

    @pinout.setter
    def pinout(self, pinout):
        llen = self._getLlen(pinout)

        self._pinout = []
        for idx, entry in enumerate(pinout):
            self._pinout.append(pinout[idx])
            # reverse order for left pins
            if idx % 2 == 0:
                self._pinout[idx].reverse()
                while len(self._pinout[idx]) < llen:
                    self._pinout[idx].insert(0, None)

    def _getLlen(self, pinout):
        """Calculate count of left pins functions
        
        return max count of it
        """
        if len(pinout):
            llen = max([len(x) for x in pinout[: len(pinout) // 2]])
        else:
            llen = 0

        return llen

    def _getRlen(self, pinout):
        """Calculate count of right pins functions
        
        return max count of it
        """
        if len(pinout):
            rlen = max([len(x) for x in pinout[len(pinout) // 2 :]])
        else:
            rlen = 0

        return rlen

    def _getStyle(self, text):
        """Find a return stlye for pin's function coloring
        
        return: style tuple (background color, foreground color)
        """
        for regexp, style in STYLLING:
            if re.match(regexp, text):
                if style in STYLES:
                    return STYLES[style]
                else:
                    # print warnning and then return default style
                    print("WARNING: Unknown style '%s'" % style)

        return STYLES["default"]

    def _pinFuncs(self, pin, X, Y):
        """Calculate position, add each funtion of pin and style it
        
        return: SVG elements list
        """
        pinFuncs = self.pinout[pin]

        def _pinLine(X, Y):
            # draw line
            linelen = len(pinFuncs)
            if pin % 2 == 1:
                offset = -self.pfSpace
            else:
                offset = 0
            X += offset
            Y += (self.pfSize + 4) // 2
            for item in pinFuncs:
                # skip None items at the start
                if item is None:
                    X += self.pfWidth + self.pfSpace
                    linelen -= 1
                else:
                    break
            pinLine = self.line(
                start=(X, Y),
                end=(X + (self.pfWidth + self.pfSpace) * linelen, Y),
                stroke="black",
                stroke_width=2,
            )
            return pinLine

        retlist = []

        # draw line
        retlist.append(_pinLine(X, Y))
        # draw pin functions
        for item in pinFuncs:
            if item is not None:
                grp = self.g()
                bgStyle, fgStyle = self._getStyle(item)
                # add func's rectangle
                grp.add(
                    self.rect(
                        insert=(X, Y),
                        size=(self.pfWidth, self.pfSize + 4),
                        fill=bgStyle,
                        stroke="black",
                        rx=5,
                        ry=5,
                    )
                )
                # add func's text
                offs = 1 if item.startswith("~") else 0
                grp.add(
                    self.text(
                        item.replace("~", ""),
                        insert=(X + self.pfWidth // 2, Y + self.pfSize + offs),
                        text_anchor="middle",
                        font_size=self.pfSize,
                        fill=fgStyle,
                    )
                )
                # draw inverting line
                if item.startswith("~"):
                    lineL = 10 * len(item.replace("~", ""))
                    lineX = X + self.pfWidth // 2 - lineL // 2
                    grp.add(
                        self.line(
                            start=(lineX, Y + 3),
                            end=(lineX + lineL, Y + 3),
                            stroke_width=1,
                            stroke="black",
                        )
                    )

                retlist.append(grp)

            # increment X
            X += self.pfWidth + self.pfSpace

        return retlist

    def _getBodyXstart(self):
        """Calculate and retun the IC body start X position
        """
        llen = self._getLlen(self.pinout)
        return self.border + (self.pfWidth + self.pfSpace) * llen

    def _getBodyYsize(self):
        """Calculate and retun the IC body height
        """
        return (self.pfSize + self.pfSpace) * (self.pincount // 2) + self.pfSpace

    def _getBodyXsize(self):
        """Calculate and retun the IC body width
        """
        return 3 * self.cnSize + 2 * self.pnSize  # cv add体宽

    ################################################################
    def _doPinNumbers(self, X, Y):  # 写pin的编号
        """Calculate and add pin numbers
        
        return: SVG elements list
        """
        Y += self.pnSize + self.pnSize // 2
        offset = 4
        retlist = []
        for idx in range(self.pincount // 2):
            # add left pin number 加左
            retlist.append(
                self.text(
                    1 + idx * 2,
                    insert=(X + offset, Y),
                    fill="white",
                    font_size=self.pnSize,
                )
            )
            # add right pin number 加右
            retlist.append(
                self.text(
                    2 + idx * 2,
                    insert=(X + self._getBodyXsize() - offset, Y),
                    fill="white",
                    font_size=self.pnSize,
                    text_anchor="end",
                )
            )

            Y += self.pfSize + self.pfSpace

        return retlist

    def _doBody(self):
        """Calculate position/size and add IC body and pin numbers.
        
        return: SVG group element
        """
        X = self._getBodyXstart()
        Y = self.border

        Xsize = self._getBodyXsize()
        Ysize = self._getBodyYsize()

        group = self.g()

        # draw body
        group.add(
            self.rect(
                insert=(X, Y), size=(Xsize, Ysize), stroke="none", fill="#00723d",
            )
        )
        # draw pin 1 marker
        #
        #

        # draw pin numbers
        for pinNumber in self._doPinNumbers(X, Y):
            group.add(pinNumber)

        return group

    def _doChipName(self):
        """Calculate position and add IC name
        
        return: SVG text element
        """
        llen = self._getLlen(self.pinout)
        # X = self._getBodyXstart() + self._getBodyXsize() // 2 + \
        # self.cnSize // 3
        # Y = self.border + self._getBodyYsize() // 2
        X = 925
        Y = 36
        chipName = self.text(
            self.name,
            insert=(X, Y),
            fill="black",
            font_size=self.cnSize,
            text_anchor="middle",
            # transform="rotate(-90 %d %d)" % (X, Y),
            transform="rotate(-0 %d %d)" % (X, Y),
        )
        return chipName

    def _doPinFuncs(self):
        """Add pin functions for ech pin
        
        return: SVG elements list
        """
        X = self.border
        Y = self.border + self.pfSize // 2

        lOffs = (
            self._getLlen(self.pinout) * (self.pfWidth + self.pfSpace) + self.pfSpace
        )
        lOffs += self._getBodyXsize()

        retlist = []

        if len(self.pinout):
            for idx in range(self.pincount // 2):
                for pinFunc in self._pinFuncs(idx * 2, X, Y):
                    retlist.append(pinFunc)
                for pinFunc in self._pinFuncs(1 + idx * 2, X + lOffs, Y):
                    retlist.append(pinFunc)

                Y += self.pfSize + self.pfSpace

        return retlist

    def doDraw(self):
        """Draw whole pinOut, with chipp name, chip body and pin functions.
        
        It doesn't save data to file, the save() method is needed.
        """
        self.add(self._doBody())
        self.add(self._doChipName())
        for pinFunc in self._doPinFuncs():
            self.add(pinFunc)

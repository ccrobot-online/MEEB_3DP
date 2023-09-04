import svgpinout
import svgwrite
import os
import cairosvg


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


LCD = [  # pin number
    ["PB5", "BEEPER",],  # 1
    ["PB6", "BTN_ENC", "PWM", "SCL"],  # 2
    ["PA2", "BTN_EN1", "PWM", "ADC", "UART2_TX"],  # 3
    ["RESET"],
    ["PA3", "BTN_EN2", "PWM", "ADC", "UART2_RX"],
    ["PB8", "LCD_CLK", "PWM"],
    ["PB7", "LCD_CS", "PWM", "SDA"],
    ["PA4", "LCD_DAT", "ADC"],
    ["GND"],
    ["VCC5"],
]

b = svgpinout.header(header_name="LCD", pinout=LCD, nameSize=32)
b.doDraw()
header = b.image(
    resource_path("header2x5_male.svg"),
    size=(10000 * 0.7, 7100 * 0.7),
    insert=(470, -40),
)
header.stretch()
b.add(header)
b.save()
cairosvg.svg2png(url=resource_path("LCD.svg"), write_to="LCD.png")
#################################################################################
OLED = [  # pin number
    ["PB5", "BEEPER",],  # 1
    ["PB6", "SCL"],  # 2
    ["PA2", "STUFF", "PWM", "ADC", "UART2_TX"],  # 3
    ["RESET"],
    ["PA3", "BTN_EN2"],
    ["PB8", "BTN_ENC"],
    ["PB7", "SDA"],
    ["PA4", "BTN_EN1"],
    ["GND"],
    ["VCC5"],
]

c = svgpinout.header(header_name="OLED", pinout=OLED, nameSize=32)
c.doDraw()
header2 = c.image(
    resource_path("header2x5_male.svg"),
    size=(10000 * 0.7, 7100 * 0.7),
    insert=(470, -40),
)
header2.stretch()
c.add(header2)
c.save()
cairosvg.svg2png(url=resource_path("OLED.svg"), write_to="OLED.png")

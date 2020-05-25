/**
 * Marlin 3D Printer Firmware
 * Copyright (C) 2019 MarlinFirmware [https://github.com/MarlinFirmware/Marlin]
 *
 * Based on Sprinter and grbl.
 * Copyright (C) 2011 Camiel Gubbels / Erik van der Zalm
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */
// #define STATUS_LOGO_X            0
// #define STATUS_LOGO_Y            0
 
/**
 * Made with Marlin Bitmap Converter
 * https://marlinfw.org/tools/u8glib/converter.html
 *
 * This bitmap from the file 'Untitled (1).svg'
 */
#pragma once

#define STATUS_LOGO_X            0
#define STATUS_LOGO_Y            0
#define STATUS_LOGO_WIDTH       39

const unsigned char status_logo_bmp[] PROGMEM = {
  B11000000,B00110011,B11111011,B11111101,B11111100, // ##........##..#######.########.#######..
  B11100000,B01110111,B11111011,B11111101,B11111110, // ###......###.########.########.########.
  B11100000,B01110110,B00000011,B00000001,B10000110, // ###......###.##.......##.......##....##.
  B11110000,B11110110,B00000011,B00000001,B10000110, // ####....####.##.......##.......##....##.
  B11110000,B11110110,B00000011,B00000001,B10000110, // ####....####.##.......##.......##....##.
  B11010000,B10110110,B00000011,B00000001,B10000110, // ##.#....#.##.##.......##.......##....##.
  B11011001,B10110111,B11111011,B11111001,B11111110, // ##.##..##.##.########.#######..########.
  B11011001,B10110110,B00000011,B00000001,B10000110, // ##.##..##.##.##.......##.......##....##.
  B11001111,B00110110,B00000011,B00000001,B10000110, // ##..####..##.##.......##.......##....##.
  B11001111,B00110110,B00000011,B00000001,B10000110, // ##..####..##.##.......##.......##....##.
  B11001111,B00110110,B00000011,B00000001,B10000110, // ##..####..##.##.......##.......##....##.
  B11000110,B00110111,B11111011,B11111101,B11111110, // ##...##...##.########.########.########.
  B11000000,B00110011,B11111001,B11111101,B11111100, // ##........##..#######..#######.#######..
  B00000000,B00000000,B00000000,B00000000,B00000000, // ........................................
  B00001111,B11100001,B11111110,B00001111,B11110000, // ....#######....########.....########....
  B00011111,B11110001,B11111111,B00001111,B11111000, // ...#########...#########....#########...
  B00011000,B00110001,B10000001,B10001100,B00011000, // ...##.....##...##......##...##.....##...
  B00000000,B00110001,B10000001,B10001100,B00011000, // ..........##...##......##...##.....##...
  B00000000,B00110001,B10000001,B10001100,B00011000, // ..........##...##......##...##.....##...
  B00000111,B11100001,B10000001,B10001100,B00011000, // .....######....##......##...##.....##...
  B00000111,B11100001,B10000001,B10001111,B11111000, // .....######....##......##...#########...
  B00000000,B00110001,B10000001,B10001111,B11110000, // ..........##...##......##...########....
  B00000000,B00110001,B10000001,B10001100,B00000000, // ..........##...##......##...##..........
  B00000000,B00110001,B10000001,B10001100,B00000000, // ..........##...##......##...##..........
  B00011000,B00110001,B10000001,B10001100,B00000000, // ...##.....##...##......##...##..........
  B00011111,B11110001,B11111111,B00001100,B00000000, // ...#########...#########....##..........
  B00001111,B11100001,B11111110,B00001100,B00000000, // ....#######....########.....##..........
  B00000000,B00000000,B00000000,B00000000,B00000000  // ........................................
};

//
// Use default bitmaps
//
#define STATUS_HOTEND_ANIM
#define STATUS_BED_ANIM
#define STATUS_HEATERS_XSPACE   20
#if HOTENDS < 2
  #define STATUS_HEATERS_X      48
  #define STATUS_BED_X          72
#else
  #define STATUS_HEATERS_X      40
  #define STATUS_BED_X          80
#endif

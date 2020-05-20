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

/**
 * Made with Marlin Bitmap Converter
 * https://marlinfw.org/tools/u8glib/converter.html
 *
 * This bitmap from the file 'Untitled (3).svg'
 */
#pragma once

//
// Status Screen Logo bitmap
//
#define STATUS_LOGO_X            0
#define STATUS_LOGO_Y            0
#define STATUS_LOGO_WIDTH       39

const unsigned char status_logo_bmp[] PROGMEM = {
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B01110011,B10001111,B11000111,B11110011,B11111100, // ▐█·█▌·███·▐███·████·
  B01110011,B10001111,B11000111,B11110011,B11111100, // ▐█·█▌·███·▐███·████·
  B01111111,B10001110,B00000111,B00000011,B10001110, // ▐███▌·█▌··▐█···█▌·█▌
  B01111111,B10001110,B00000111,B00000011,B10001100, // ▐███▌·█▌··▐█···█▌·█·
  B01111111,B10001110,B00000111,B00000011,B10001110, // ▐███▌·█▌··▐█···█▌·█▌
  B01111111,B10001110,B00000111,B00000011,B10001100, // ▐███▌·█▌··▐█···█▌·█·
  B01111111,B10001111,B11000111,B11110011,B11111000, // ▐███▌·███·▐███·███▌·
  B01111111,B10001111,B11000111,B11110011,B11111100, // ▐███▌·███·▐███·████·
  B01111101,B10001110,B00000111,B00000011,B10001110, // ▐██▐▌·█▌··▐█···█▌·█▌
  B01111101,B10001110,B00000111,B00000011,B10001100, // ▐██▐▌·█▌··▐█···█▌·█·
  B01111101,B10001110,B00000111,B00000011,B10001110, // ▐██▐▌·█▌··▐█···█▌·█▌
  B01111101,B10001111,B11000111,B11110011,B11111100, // ▐██▐▌·███·▐███·████·
  B01110001,B10001111,B11000111,B11110011,B11111100, // ▐█·▐▌·███·▐███·████·
  B01100001,B10001111,B11000011,B11110011,B11111100, // ▐▌·▐▌·███··███·████·
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B11111000,B11111100,B00111111,B10000000, // ····██▌·███··███▌···
  B00000000,B11111100,B11111110,B00111111,B10000000, // ····███·███▌·███▌···
  B00000001,B11111110,B11111111,B00111111,B11000000, // ···▐███▌████·████···
  B00000001,B11001110,B11100111,B00111001,B11000000, // ···▐█·█▌█▌▐█·█▌▐█···
  B00000000,B00001110,B11100011,B10111001,B11000000, // ······█▌█▌·█▌█▌▐█···
  B00000000,B00001110,B11100011,B10111001,B11000000, // ······█▌█▌·█▌█▌▐█···
  B00000000,B01111100,B11100011,B10111111,B10000000, // ····▐██·█▌·█▌███▌···
  B00000000,B01111100,B11100011,B10111111,B10000000, // ····▐██·█▌·█▌███▌···
  B00000000,B00001110,B11100011,B10111000,B00000000, // ······█▌█▌·█▌█▌·····
  B00000000,B00001110,B11100011,B10111000,B00000000, // ······█▌█▌·█▌█▌·····
  B00000001,B11001110,B11100111,B00111000,B00000000, // ···▐█·█▌█▌▐█·█▌·····
  B00000001,B11001110,B11100111,B00111000,B00000000, // ···▐█·█▌█▌▐█·█▌·····
  B00000000,B11111100,B11111110,B00111000,B00000000, // ····███·███▌·█▌·····
  B00000000,B11111000,B11111100,B00111000,B00000000, // ····██▌·███··█▌·····
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000  // ····················
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

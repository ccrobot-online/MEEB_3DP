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
 * This bitmap from the file 'status_logo.svg'
 */
#pragma once

#define STATUS_LOGO_X            0
#define STATUS_LOGO_Y            0
#define STATUS_LOGO_WIDTH        39

const unsigned char status_logo_bmp[] PROGMEM = {
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B11100000,B01100011,B11110011,B11110011,B11110000, // █▌··▐▌·███·███·███··
  B11100000,B11100011,B11110011,B11110011,B11111000, // █▌··█▌·███·███·███▌·
  B11100000,B11100011,B00000011,B00000011,B00001100, // █▌··█▌·█···█···█··█·
  B11110000,B11100011,B00000011,B00000011,B00001100, // ██··█▌·█···█···█··█·
  B11110001,B11100011,B00000011,B00000011,B00011000, // ██·▐█▌·█···█···█·▐▌·
  B11010001,B11100011,B11110011,B11110011,B11111000, // █▐·▐█▌·███·███·███▌·
  B11011011,B01100011,B00000011,B00000011,B00011100, // █▐▌█▐▌·█···█···█·▐█·
  B11011011,B01100011,B00000011,B00000011,B00001100, // █▐▌█▐▌·█···█···█··█·
  B11001110,B01100011,B00000011,B00000011,B00001100, // █·█▌▐▌·█···█···█··█·
  B11001110,B01100011,B00000011,B00000011,B00011100, // █·█▌▐▌·█···█···█·▐█·
  B11000110,B01100011,B11110011,B11111011,B11111000, // █·▐▌▐▌·███·███▌███▌·
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B01111001,B11100011,B00111001,B11100000,B00000000, // ▐█▌▐█▌·█·█▌▐█▌······
  B01001111,B00000011,B00000100,B00100000,B00000000, // ▐·██···█··▐··▌······
  B01001101,B00000101,B00001100,B00100000,B00000000, // ▐·█▐··▐▐··█··▌······
  B01111000,B11001101,B00001000,B01100000,B00000000, // ▐█▌·█·█▐··▌·▐▌······
  B01011000,B00101001,B00010000,B11000000,B00000000, // ▐▐▌··▌▌▐·▐··█·······
  B01001000,B00101111,B00100001,B10000000,B00000000, // ▐·▌··▌██·▌·▐▌·······
  B01001101,B11100001,B01111101,B11110000,B00000000, // ▐·█▐█▌·▐▐██▐██······
  B00000000,B00000000,B00000000,B00000000,B00000000, // ····················
  B00000000,B00000000,B00000000,B00100000,B01000000, // ·············▌··▐···
  B00000000,B00000000,B00001111,B00111110,B01111000, // ··········██·██▌▐█▌·
  B00000000,B00000000,B00000001,B00100010,B01001100, // ···········▐·▌·▌▐·█·
  B00000000,B00000000,B00000111,B00100011,B01001000, // ··········▐█·▌·█▐·▌·
  B00000000,B00000000,B00000111,B00100011,B01111000, // ··········▐█·▌·█▐█▌·
  B00000000,B00000000,B00000001,B10100010,B01000000, // ···········▐▌▌·▌▐···
  B00000000,B00000000,B00000001,B00100110,B01000000, // ···········▐·▌▐▌▐···
  B00000000,B00000000,B00001111,B00111100,B01000000  // ··········██·██·▐···
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

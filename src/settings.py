#!/usr/bin/env python
# -*- coding: utf-8 -*-


TEMP_PHOTO_DIR = 'photo_temp'

PREFIX_PHOTO_NAME = 'photo_'

AUTO_PRINT = False

PATCH_BACKGROUND_IMG = 'media/background-default.jpg'

PATCH_LOGO_IMG = 'media/logo.png'

PAPER_SIZE_OPTION = {
    1: 'legal',
    2: 'letter',
    3: 'A3',
    4: 'A4',
    5: 'A5',
    6: 'A6',
    7: 'exec',
    8: 'ledger',
    9: '11x17',
    10: 'B4-JIS',
    11: 'B5-JIS',
    12: 'B5-ISO',
    13: 'B6-JIS',
    14: 'com10',
    15: 'com10env',
    16: 'PostCard Single',
    17: 'PostCard Double',
    18: 'custom',
    19: 'C5',
    20: 'C5env',
    21: 'DL',
    22: 'DLenv',
    23: 'monarch'
}

PAPER_SIZE = PAPER_SIZE_OPTION[4]

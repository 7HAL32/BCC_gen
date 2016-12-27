#!/usr/bin/env python3

"""
Package: 7HAL32/BCC_generator

Public version of the Bar Code Card Generator. Converts binary sequences into bar code-like, printable PDF files. Intended to be used with the Linear Hamming Code Generator (7HAL32/LHC_generator).

This tool is used to create the bar code cards that contain instructions for the stack machine robot which is designed, assembled and programmed by students during the NES RoboLab course at Technische Universität Dresden. Specifications and further information can be found at http://robolab.inf.tu-dresden.de (reachable from within campus network).

NOTE: Currently only supports direct, raw binary input via files.

Developed as part of the NES RoboLab Project at Technische Universität Dresden.
Handcrafted with :heart: by Lutz Thies in 2016.
"""

import cairosvg
import glob
import os
import svgwrite
import svgutils.compose

__author__ = "Lutz Thies"
__copyright__ = "Copyright (c) 2016"
__credits__ = ["Lutz Thies"]

__license__ = "MIT"
__version__ = "0.9.2"
__maintainer__ = "Lutz Thies"
__email__ = "lutz.thies@tu-dresden.de"
__status__ = "Pre-Release"


class BarcodeCard:
    def __init__(self, width=105, height=297, margin=15, offset=60, bits=10, length=20, space=30):
        """
        Prepares an empty barcode card with the specified dimensions
        Default is DIN A4.

        :param width: integer (width on paper in millimeters)
        :param height: integer (height on paper in millimeters)
        :param margin: integer (left and right margin in millimeters)
        :param offset: integer (top margin of first bar)
        :param bits: integer (number of bits)
        :param length: integer (vertical height of a block)
        :param space: integer (vertical padding between two bars)
        :returns:
        """
        # usable space on paper
        effective_size = width - 2 * margin
        # number of blocks, increased by one for the SYN block
        self.blockcount = bits + 1
        self.blocksize = effective_size / self.blockcount
        stripesize = self.blocksize / 2

        self.space = space
        self.x = margin
        self.margin = margin
        self.y = offset
        self.stripesize = stripesize
        self.length = length
        # final dimensions on paper
        self.svg = svgwrite.Drawing(size=(str(width) + 'mm', str(height) + 'mm'))
        # actual coordinate system, may be increased for higher accuracy
        self.svg.viewbox(width=width, height=height)

    def add_bar(self, word):
        """
        Appends a new bar to the card

        :param word: string (contains bit sequence)
        :returns: %
        """
        bits = list(map(int, word))
        # write SYN bit
        self._add_block(1)
        # write following bits of the word
        for i in range(0, self.blockcount - 1):
                self._add_block(bits[i])
        # bar is finished, reset x and add space
        self.x = self.margin
        self.y += self.space

    def _add_block(self, bit):
        """
        Appends a new block to the current bar

        :param bit: integer (either 0 or 1, for unset or set bit)
        :returns: %
        """
        if bit:
            self.svg.add(self.svg.rect(insert=(self.x, self.y), size=(self.stripesize, self.length), fill="rgb(0,0,0)"))
        # move to next block position
        self.x += self.blocksize

    def save(self, filename):
        """
        Dumps the SVG, i.e. the card, to the specified file

        :param filename: string (path to the file, will be created if non-existent)
        :returns: %
        """
        self.svg.saveas(filename)


def chunk(l, size):
    """
    Splits a list into chunks of specified size

    Credits to Frank Busse for the smart list comprehension

    :param l: list
    :param size: integer (size of each chunk)
    :returns: list of lists
    """
    return [l[i:i + size] for i in range(0, len(l), size)]


def from_file(path):
    # read encoded words
    with open(path, 'r') as f:
        # ignore comments
        lines = [line.rstrip('\n') for line in f if not line.startswith('#')]
    # split into blocks that fit on one card
    code_blocks = chunk(lines, size=6)
    # print two cards on a single sheet of paper (DIN A4)
    for index, block in enumerate(chunk(code_blocks, size=2)):
        for i, code_block in enumerate(block):
            card = BarcodeCard()
            for word in code_block:
                card.add_bar(word)
            card.save("_temp_" + str(i) + ".svg")
        # mod 2
        if os.path.isfile("./_temp_1.svg"):
            # compose two cards
            svgutils.compose.Figure("210mm", "297mm", svgutils.compose.SVG("_temp_0.svg"), svgutils.compose.SVG("_temp_1.svg").move(105, 0)).save("card_" + str(index) + ".svg")
        else:
            os.rename("_temp_0.svg", "card_" + str(index) + ".svg")
        # save final page
        cairosvg.svg2pdf(file_obj=open("card_" + str(index) + ".svg", "rb"), write_to="card_" + str(index) + ".pdf")
    # remove temporary files
    for f in glob.glob("_*.svg"):
        os.remove(f)

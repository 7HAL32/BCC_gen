#!/usr/bin/env python3

"""
Package: 7HAL32/BCC_generator

Example for the Bar Code Card Generator. Demonstrates the generation of 4 bar code cards onto 2 sheets of paper from a file. Input and expected output are provided in the './sample/' directory.

Specifications and further information can be found at http://robolab.inf.tu-dresden.de (reachable from within campus network).

Developed as part of the NES RoboLab Project at Technische Universität Dresden.

Handcrafted with :heart: by Lutz Thies in 2016.
"""

import argparse
import sys
from BCC_generator import bcc_generator


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", dest="path",
                        help="input file containing binary sequences that will be printed")
    args = parser.parse_args()
    if not len(sys.argv) > 1:
        print("No input file was given as argument, generating cards from sample.")
        bcc_generator.from_file('./sample/input.txt')
    else:
        print("Generating cards from", args.path, ".")
        bcc_generator.from_file(args.path)

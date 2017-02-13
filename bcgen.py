#!/usr/bin/env python3

# create at most two cards with 6 rows of 11 bars
#
# usage: ./bcgen.py card0.txt card1.txt ...
#
# file format:
# 0110011101
# 10010101101
# ...

from pathlib import Path
from sys import argv

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

# bars
cols = 11
rows = 6

assert cols > 0, "card should have at least one bar per line"
assert rows > 0, "card should have at least one row of bars"

# dimensions
width, height = A4
bar_h = 20 * mm
bar_w = 3.5 * mm
space_h = 3.5 * mm
space_v = 10 * mm
marker = 5 * mm

# origins
x_left = (width / 2 - cols * bar_w - (cols - 1) * space_h) / 2
y_left = (height - rows * bar_h - (rows - 1) * space_v) / 2 + (rows - 1) * bar_h + (rows - 1) * space_v
x_right = width / 2 + x_left
y_right = y_left

assert x_left >= 0, "bars don't fit on row"
assert y_left + bar_h <= height, "rows don't fit on card"

# colours
col_bar = 0,0,0
col_mkr = 0.7,0.7,0.7


def draw_card(canvas, lines, x0, y0):
	canvas.setFillColorRGB(*col_bar)
	canvas.setStrokeColorRGB(*col_bar)

	for i, line in enumerate(lines):
		y = y0 - i * (bar_h + space_v)

		# prepend SYN bit if necessary
		if len(line) == cols - 1:
			line = ['1'] + line
		assert len(line) == cols, "only 10 or 11 bars per line permitted"
		assert line[0] == '1', "SYN bit is 0"

		for k, bar in enumerate(line):
			x = x0 + k * (bar_w + space_h)
			if bar == '1':
				canvas.rect(x, y, bar_w, bar_h, stroke=0, fill=1)


def draw_markers(canvas, two):
	canvas.setFillColorRGB(*col_bar)

	# draw border markers
	o = 0.5
	for (x,y) in [(x,y) for x in [o, width - o] for y in [o, height - o]]:
		canvas.line(x - marker, y, x + marker, y)
		canvas.line(x, y - marker, x, y + marker)

	canvas.setFillColorRGB(*col_mkr)

	# draw arrows
	canvas.drawCentredString(0.25 * width, height - 32, "\u2193")
	if two:
		canvas.drawCentredString(0.75 * width, height - 32, "\u2193")

	canvas.setStrokeColorRGB(*col_mkr)

	# draw cut line
	canvas.setLineWidth(0.3)
	canvas.setDash(6,3)
	canvas.line(width / 2, 0, width / 2, height)


def draw_name(canvas, name, two):
	canvas.setFillColorRGB(*col_mkr)

	canvas.drawCentredString(0.25 * width, 20, name + " (1)")
	if two:
		canvas.drawCentredString(0.75 * width, 20, name + " (2)")

def main(files):
	for fname in files:
		# read file
		f = open(fname)
		p = Path(fname)
		lines = list(map(list, f.read().splitlines()))
		f.close()
		assert len(lines) <= 2 * rows, "too many lines for two cards"
		two = len(lines) > rows

		# create canvas
		c = Canvas(str(p.with_suffix(".pdf")), pagesize=A4)
		c.setFont("Helvetica", 12)

		# draw markers
		draw_markers(c, two)

		# draw cards
		draw_card(c, lines[0:rows],  x_left,  y_left)
		draw_card(c, lines[rows:2*rows], x_right, y_right)

		# add names
		draw_name(c, p.stem, two)

		# save pdf
		c.save()


if __name__ == "__main__":
	main(argv[1:])

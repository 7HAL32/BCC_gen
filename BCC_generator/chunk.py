"""
Universal quick and dirty chunk function, which turned out to be extremely useful in lots of cases.

Handcrafted with :heart: by Lutz Thies in 2016.
"""

__author__ = "Lutz Thies"
__copyright__ = "Copyright (c) 2016"
__credits__ = ["Lutz Thies"]

__license__ = "MIT"
__version__ = "1.0.2"
__maintainer__ = "Lutz Thies"
__email__ = "lutz.thies@tu-dresden.de"
__status__ = "Release"


def chunk(enum, size):
    """
    Splits an enum into chunks of specified size
    :param enum: enum (e.g. list)
    :param size: integer (size of each chunk)
    :return: list of lists (chunks)
    """
    chunks = []
    for index, split in enumerate(enum):
        if index % size == 0:
            chunks.append([])
        chunks[index // size].append(split)
    return chunks

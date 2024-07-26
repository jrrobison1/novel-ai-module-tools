#!/usr/bin/env python3
import sys
import os
from os import walk
from matplotlib import pyplot
import numpy as np

try:
    working_directory = sys.argv[1]
    print(working_directory)
except:
    print("Please pass directory name")
    exit(1)

# Get edited file list
stitched_directory = os.path.join(working_directory, "names_replaced", "stitched")
filenames = next(walk(stitched_directory), (None, None, []))[2]  # [] if no file
for filename in filenames:
    if filename.startswith("." or not filename.endswith(".txt")):
        filenames.remove(filename)

books = {}
authors = {}
total_file_size = 0

# Gather file data
for filename in filenames:
    # Split filename
    author = filename.split("_")[1].replace("-", " ")
    book = filename.split("_")[2].split(".")[0].replace("-", " ")

    # Get file size in bytes
    file_size = os.path.getsize(os.path.join(stitched_directory, filename))

    if author not in authors:
        authors[author] = file_size
    else:
        authors[author] += file_size

    if book not in books:
        books[book] = file_size
    else:
        books[book] += file_size

    total_file_size += file_size


# Construct the book and author graphs
# Author graph
author_labels = []
author_sizes = []
for x, y in authors.items():
    author_labels.append(x + " (" "{:.1f}".format((y / total_file_size) * 100) + "%)")
    author_sizes.append(y)

fig1, ax1 = pyplot.subplots()
ax1.pie(author_sizes, labels=author_labels)
ax1.set_title("Author Influences", fontweight="bold")
fig1.savefig("authors.png", bbox_inches="tight")
pyplot.close(fig1)


# Book graph
book_labels = []
book_sizes = []
for x, y in books.items():
    book_labels.append(x + " (" "{:.1f}".format((y / total_file_size) * 100) + "%)")
    book_sizes.append(y)

fig2, ax2 = pyplot.subplots()
ax2.pie(book_sizes, labels=book_labels)
ax2.set_title("Book Influences", fontweight="bold")
fig2.savefig("books.png", bbox_inches="tight")
pyplot.close(fig2)

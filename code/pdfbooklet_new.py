#!/usr/bin/python

# pdfbooklet.py
#
# Copyright (c) 2014 Mark O. Busby <mark@busbycreations.com>
#
# Licensed under the MIT/X11 license - see LICENSE.txt
#
# Create booklet from selected pdf file, in selected page range
# Depends on pyPDF2


# I made some changes. dvir gimdani, 2022.

# from optparse import OptionParser
# import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.pdf import PageObject


def pdfbooklet(pdfIn, pdfOut, firstPage=1, lastPage=0, booklet=1, eng=0, debug=False):
    # Get numPagesInFile using PyPDF
    pdfi = open(pdfIn, 'rb')
    pdfReader = PdfFileReader(pdfi)
    numPagesInFile = pdfReader.getNumPages()
    pageSize = pdfReader.getPage(firstPage).mediaBox.upperRight
    if debug: print("numPagesInFile: " + str(numPagesInFile))

    if lastPage <= 0:
        lastPage = numPagesInFile
    else:
        lastPage = lastPage

    if lastPage > numPagesInFile:
        lastPage = numPagesInFile

    numPages = 1 + lastPage - firstPage
    if debug: print("numPages: " + str(numPages))
    numSheets = numPages / 4
    if debug: print("numSheets: " + str(numSheets))
    if (numPages % 4 > 0):
        # if ((numPages > 4) & ((numPages % 4 > 0) | (numSheets == 0))):
        if debug:
            print("numPages % 4 = " + str(numPages % 4))
            print("Adding extra sheet.")
        numSheets += 1
    if debug: print("numSheets: " + str(numSheets))

    pagesToPrint = numSheets * 4
    numBlankPages = pagesToPrint - numPages
    frontOffset = 0
    backOffset = 1

    if booklet == 1:
        pagesInOrder = []
        pagesInOrder.append(firstPage + pagesToPrint - 1)
        if debug: print("pagesToPrint: " + str(pagesToPrint))
        while len(pagesInOrder) < pagesToPrint:
            pagesInOrder.append(firstPage + frontOffset)
            pagesInOrder.append(firstPage + 1 + frontOffset)
            frontOffset += 2
            pagesInOrder.append(firstPage + pagesToPrint - 1 - backOffset)
            pagesInOrder.append(firstPage + pagesToPrint - 1 - backOffset - 1)
            backOffset += 2
        del (pagesInOrder[len(pagesInOrder) - 1])
        # swap to hebrew order
        for i in range(0, len(pagesInOrder), 2):
            tmp = pagesInOrder[i]
            pagesInOrder[i] = pagesInOrder[i + 1]
            pagesInOrder[i + 1] = tmp
    else:
        pagesInOrder = [i + firstPage for i in range(lastPage)]
    if eng == 1:
        for i in range(0, len(pagesInOrder), 2):
            tmp = pagesInOrder[i]
            pagesInOrder[i] = pagesInOrder[i + 1]
            pagesInOrder[i + 1] = tmp

    if debug: print(pagesInOrder)
    # Create 2-per-page PDF, ready for printing
    # This is done by creating a side-ways page, and overlaying two scaled pages
    # on top.  US Letter is 612 x 792 pts (portrait)
    x = float(pageSize[0])
    y = float(pageSize[1])
    xPrime = 842  # 792
    yPrime = 595  # 612
    scale = 0.5 * xPrime / x
    scale2 = yPrime / y
    if (scale > scale2): scale = scale2
    yOffset = (yPrime - scale * y) / 2
    yOffsetLeft = yOffset
    xOffsetLeft = (xPrime - 2 * scale * x) / 4
    xOffset = xOffsetLeft + xPrime / 2

    # detecting if pages are already landscape
    landscape = False
    if x > y:
        landscape = True
        xPrime = 595  # 612
        yPrime = 842  # 792
        scale = 0.5 * yPrime / y
        scale2 = xPrime / x
        if (scale > scale2): scale = scale2
        xOffset = (xPrime - scale * x) / 2
        xOffsetLeft = xOffset
        yOffset = (yPrime - 2 * scale * y) / 4
        yOffsetLeft = yOffset + yPrime / 2

    if debug: print('landscape: ', landscape)
    if debug: print('x: ', x)
    if debug: print('y: ', y)
    if debug: print('xPrime: ', xPrime, xPrime / 2)
    if debug: print('yPrime: ', yPrime, yPrime / 2)
    if debug: print('scale: ', scale, scale * x, scale * y)
    if debug: print('xOffset: ', xOffset)
    if debug: print('yOffset: ', yOffset)
    if debug: print('xOffsetLeft: ', xOffsetLeft)
    if debug: print('yOffsetLeft: ', yOffsetLeft)

    writer = PdfFileWriter()
    leftPage = True
    for pageNum in pagesInOrder:
        if pageNum > lastPage:
            page = PageObject.createBlankPage(width=x, height=y)
        else:
            page = pdfReader.getPage(int(pageNum - 1))

        if leftPage == True:
            combinedPage = PageObject.createBlankPage(width=xPrime, height=yPrime)
            combinedPage.mergeScaledTranslatedPage(page, scale, xOffsetLeft, yOffsetLeft)
        else:
            combinedPage.mergeScaledTranslatedPage(page, scale, xOffset, yOffset)
            writer.addPage(combinedPage)

        leftPage = not leftPage

    pdfo = open(pdfOut, 'wb')
    writer.write(pdfo)

    pdfi.close()
    pdfo.close()
    # print("Completed!  Booklet is in " + pdfOut)

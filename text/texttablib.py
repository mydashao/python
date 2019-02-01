import tablib

data = tablib.Dataset()
names = ['Kenneth Reitz', 'Bessie Monke']

for name in names:
    # split name appropriately
    fname, lname = name.split()

    # add names to Dataset
    data.append([fname, lname])

    data.dict
    data.headers = ['First Name', 'Last Name']
    data.dict

    data.export("D:\IMDB.xlsx")
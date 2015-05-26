#!/usr/bin/python

n = 19
if n <= 10:
    total = 0
    j = 1
    if j <= n:
        i = 1
        while i <= j:
            total = total + i
            i = i + 1
        j = j + 1
        print total
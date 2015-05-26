#!/usr/bin/python

#adapted from answer5.py but for strings

answer = 41
str = "p"
str2 = "q"
if str > "a": answer = answer + 2
if "p" >= str: answer = answer + 2
if str > 'z': answer = answer + 2
if 'p' >= str: answer = answer + 2
if "a" < "p": answer = answer + 2
if 'a' < 'p': answer = answer + 2
if str > str2: answer = answer + 2
if 'z' <= "a": answer = answer + 2
if str == 'a': answer = answer - 1
if "x\"" != 'str': answer = answer + 1
if str2 <> "p": answer = answer + 1
print answer


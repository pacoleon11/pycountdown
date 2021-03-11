#!/usr/bin/env python3
import time
import curses

"""    The tuple items are:
      year (including century, e.g. 1998)
      month (1-12)
      day (1-31)
      hours (0-23)
      minutes (0-59)
      seconds (0-59)
      weekday (0-6, Monday is 0)
      Julian day (day in the year, 1-366)
      DST (Daylight Savings Time) flag (-1, 0 or 1)
"""
end = time.mktime((2021, 1, 20, 9, 0, 0, 0, 0, 0))
waitt = (4 * 365 + 1) *24*60*60

prec = 2

arts = """
 ▓▓▓▓▓▓    ▓▓    ▓▓▓▓▓▓  ▓▓▓▓▓▓ ▓▓    ▓▓▓▓▓▓▓▓▓  ▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓  ▓▓▓▓▓▓                 ▓▓    ▓▓
▓▓▓   ▓▓ ▓▓▓▓   ▓▓    ▓▓▓▓    ▓▓▓▓    ▓▓▓▓      ▓▓    ▓▓     ▓▓ ▓▓    ▓▓▓▓    ▓▓                     ▓▓ 
▓▓▓▓  ▓▓   ▓▓         ▓▓      ▓▓▓▓    ▓▓▓▓      ▓▓          ▓▓  ▓▓    ▓▓▓▓    ▓▓   ▓▓               ▓▓  
▓▓ ▓▓ ▓▓   ▓▓    ▓▓▓▓▓▓   ▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓    ▓▓    ▓▓▓▓▓▓  ▓▓▓▓▓▓▓                   ▓▓   
▓▓  ▓▓▓▓   ▓▓   ▓▓            ▓▓      ▓▓      ▓▓▓▓    ▓▓  ▓▓    ▓▓    ▓▓      ▓▓                  ▓▓    
▓▓   ▓▓▓   ▓▓   ▓▓      ▓▓    ▓▓      ▓▓▓▓    ▓▓▓▓    ▓▓ ▓▓     ▓▓    ▓▓▓▓    ▓▓   ▓▓            ▓▓     
 ▓▓▓▓▓▓  ▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓       ▓▓ ▓▓▓▓▓▓  ▓▓▓▓▓▓ ▓▓       ▓▓▓▓▓▓  ▓▓▓▓▓▓            ▓▓   ▓▓    ▓▓
"""

def get_art(i):
    return '\n'.join(line[8*i:8*(i+1)] for line in filter(None, arts.splitlines()))

def concat_art(arts):
    arts = [a.splitlines() for a in arts]
    arts = [' '.join(l) for l in zip(*arts)]
    return arts

def main(window):

    try:
        while True:
            now = time.time()
            wait = end - now
            wptg = 100 - wait / waitt * 100

            wait, s = divmod(wait, 60)
            wait, m = divmod(wait, 60)
            d,    h = divmod(wait, 24)
            ss      = (s%1)*(10**prec)
            wptgf = (wptg%1)*(10**prec)
            wptgi = int(wptg)

            d  = str(int(d))
            h  = format(int(h), '02d')
            m  = format(int(m), '02d')
            s  = format(int(s), '02d')
            ss = format(int(ss), '0{}d'.format(prec))

            wptgi = format(int(wptgi), '02d')
            wptgf = format(int(wptgf), '0{}d'.format(prec))

            wait = []
            for i in map(int, d):  wait.append(get_art(i))
            wait.append(get_art(10))
            for i in map(int, h):  wait.append(get_art(i))
            wait.append(get_art(10))
            for i in map(int, m):  wait.append(get_art(i))
            wait.append(get_art(10))
            for i in map(int, s):  wait.append(get_art(i))
            if prec:
                wait.append(get_art(11))
                for i in map(int, ss): wait.append(get_art(i))
            wait = concat_art(wait)

            wait2 = []
            for i in map(int, wptgi):  wait2.append(get_art(i))
            wait2.append(get_art(11))
            for i in map(int, wptgf):  wait2.append(get_art(i))
            wait2.append(get_art(12))
            wait2 = concat_art(wait2)


            ymax, xmax = window.getmaxyx()
            y = len(wait)+2+len(wait2)
            x = len(wait[0])
            hoff = xmax//2 - x//2
            voff = ymax//2 - y//2

            for i, l in enumerate(wait):
                window.addstr(voff+i, hoff, l)

            x2 = len(wait2[0])
            hoff2 = xmax//2 - x2//2
            voff2 = voff + len(wait) + 2

            for i, l in enumerate(wait2):
                window.addstr(voff2+i, hoff2, l)

            window.refresh()
            time.sleep(10**-prec)

            for i in range(y):
                window.addstr(voff+i, hoff, ' '*x)

    except KeyboardInterrupt:
        print()


curses.wrapper(main)

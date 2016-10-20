#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from veebo.Veebo import Veebo

def main():
    veebo = Veebo()
    veebo.start()
    while True:
        try:
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            break

    veebo.quit()
    print "Quitting Veebo"

if __name__ == "__main__":
    main()

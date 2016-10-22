#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from veebo.Veebo import Veebo

def main():
    veebo = Veebo()
    veebo.start()
    while True:
        try:
            if veebo.is_stopping:
                break;
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            break

    if not veebo.is_stopping:
        veebo.quit()

    print "Quitting Veebo"

if __name__ == "__main__":
    main()

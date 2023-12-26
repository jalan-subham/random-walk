
# -*- coding: utf-8 -*-

# This file calls variables defined in globe.py,
# and functions defined in utility.py

def main():

    utility.init_game()
    utility.game_loop()


if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath("./src/"))

    # from code import utility
    # import code.utility as utility
    from src import utility

    main()

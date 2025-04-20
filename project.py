import argparse
import sys

from src.game import Game

def main():
    args = defineArgs()
    name = None
    if args.offline:
        name = get_user_name()


    game = Game(fullscreen=args.fullscreen, offline=args.offline, player_name=name)
    game.run()

def defineArgs():
    parser = argparse.ArgumentParser(description="Run game")
    parser.add_argument("-f", "--fullscreen", action="store_true", help="Enable fullscreen mode")
    parser.add_argument("-o", "--offline", action="store_true", help="Disable online features")
    args = parser.parse_args()

    return args

def get_user_name():
    while True:
        name = input("Enter your name: ")
    
        if is_name_invalid(name):
            sys.exit("Name must be between 3 and 10 characters long and cannot be empty.")
        else:
            return name

def is_name_invalid(name):
    return not name or name.isspace() or len(name) > 10 or len(name) < 3
    

if __name__ == "__main__":
    main()
import argparse

from src.game import Game

def main():
    parser = argparse.ArgumentParser(description="Run game")
    parser.add_argument("-f", "--fullscreen", action="store_true", help="Enable fullscreen mode")
    args = parser.parse_args()
    
    game = Game(fullscreen=args.fullscreen)
    game.run()
    

if __name__ == "__main__":
    main()
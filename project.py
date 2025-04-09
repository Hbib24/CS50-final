import argparse

from src.game import Game

def main():
    parser = argparse.ArgumentParser(description="Run game")
    parser.add_argument("-f", "--fullscreen", action="store_true", help="Enable fullscreen mode")
    parser.add_argument("-o", "--offline", action="store_true", help="Disable online features")
    args = parser.parse_args()
    
    game = Game(fullscreen=args.fullscreen, offline=args.offline)
    game.run()
    

if __name__ == "__main__":
    main()
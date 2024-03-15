import argparse
from discord_api_key import DISCORD_API_KEY

def main(args):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Echo Byte Discord Bot")

    # Parse arguments
    args = parser.parse_args()
    main(args)
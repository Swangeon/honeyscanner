import argparse
import re
import time

from art import ascii_art_honeyscanner
from core import Honeyscanner


def sanitize_string(s):
    s = s.strip()
    s = s.lower()
    # Remove special characters using regex (it matches any character that is
    # not a lowercase letter, a number, a space, a dot, an underscore, or a
    # hyphen and removes it.)
    s = re.sub(r'[^a-z0-9._\- ]', '', s)
    return s


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Honeyscanner: A vulnerability analyzer for honeypots"
    )
    parser.add_argument(
        "--honeypot",
        type=sanitize_string,
        required=True,
        choices=["cowrie", "kippo", "dionaea", "conpot"],
        help="Honeypot to analyze, currently supported: (cowrie, kippo, dionaea and conpot)",
    )
    parser.add_argument(
        "--honeypot_version",
        type=sanitize_string,
        required=True,
        help="The version of the honeypot to analyze",
    )
    parser.add_argument(
        "--target_ip",
        type=sanitize_string,
        required=True,
        help="The IP address of the honeypot to analyze",
    )
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="The port to connect to the honeypot to analyze",
    )
    parser.add_argument(
        "--username",
        type=str,
        required=False,
        help="The username to connect to the honeypot",
    )
    parser.add_argument(
        "--password",
        type=str,
        required=False,
        help="The password to connect to the honeypot",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    print(ascii_art_honeyscanner())
    honeyscanner = Honeyscanner(args.honeypot,
                                args.honeypot_version,
                                args.target_ip,
                                args.port,
                                args.username,
                                args.password)

    sleep_time = 5
    print(f"Starting in {sleep_time} seconds...")
    time.sleep(sleep_time)

    try:
        honeyscanner.run_all_attacks()
    except Exception as e:
        print(f"An error occurred during the attacks: {e}")
        return

    try:
        honeyscanner.generate_evaluation_report()
    except Exception as e:
        print(f"An error occurred during report generation: {e}")
        return


if __name__ == "__main__":
    # TODO: fix the report
    main()

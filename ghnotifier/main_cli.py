import schedule
import time

from handler import job

def main():
    schedule.every(5).minutes.do(job)

    while True:
        schedule.run_pending()

if __name__ == "__main__":
    main()

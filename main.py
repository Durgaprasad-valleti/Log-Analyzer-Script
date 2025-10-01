# main.py
import random
import time
import argparse
from loader import load_hostnames, load_dates, load_timelapse
from log_entry import make_log, generate_timestamps
from csv_writer import save_logs_csv
from config import HOSTFILE, DATEFILE, TIMELAPSEFILE, OUTPUT_CSV, PER_HOST, SEED

def main():
    parser = argparse.ArgumentParser(description="Generate allowed FortiGate logs CSV")
    parser.add_argument("--hostfile", default=HOSTFILE)
    parser.add_argument("--datefile", default=DATEFILE)
    parser.add_argument("--timelapsefile", default=TIMELAPSEFILE)
    parser.add_argument("--per-host", type=int, default=PER_HOST)
    parser.add_argument("--out", default=OUTPUT_CSV)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    hosts = load_hostnames(args.hostfile)
    dates_raw = load_dates(args.datefile)
    timemin, timemax = load_timelapse(args.timelapsefile)

    timestamps = generate_timestamps(len(hosts), args.per_host, dates_raw, timemin, timemax)

    logs = []
    for i, ts in enumerate(timestamps):
        host = hosts[i % len(hosts)]  # rotate hostnames
        log = make_log(host, ts)
        logs.append(log)

    save_logs_csv(logs, args.out)
    print(f"✅ Generated {len(logs)} logs in {args.out}")

if __name__ == "__main__":
    main()

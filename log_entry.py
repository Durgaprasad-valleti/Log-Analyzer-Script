# log_entry.py
import random
from datetime import datetime, timedelta

def rand_private_ip():
    return f"10.1.100.{random.randint(2,254)}"

def rand_public_ip():
    return f"172.217.{random.randint(0,255)}.{random.randint(1,254)}"

def event_ns(dt: datetime):
    epoch = datetime(1970,1,1)
    delta = dt - epoch
    return int(delta.total_seconds() * 1_000_000_000)

def make_log(hostname, timestamp_dt):
    srcip = rand_private_ip()
    dstip = rand_public_ip()
    srcport = random.randint(49152, 65535)
    dstport = random.choice([443, 80, 8080])
    sessionid = random.randint(1000, 999999)
    policyid = random.choice([1,2,3,5,10,20])
    dt = timestamp_dt
    return {
        "date": dt.strftime("%Y-%m-%d"),
        "time": dt.strftime("%H:%M:%S"),
        "logid": str(random.randint(1000000000, 9999999999)),
        "type": "utm",
        "subtype": "webfilter",
        "eventtype": "ftgd_allow",
        "level": "notice",
        "vd": "vdom1",
        "eventtime": event_ns(dt),
        "policyid": policyid,
        "sessionid": sessionid,
        "srcip": srcip,
        "srcport": srcport,
        "srcintf": "port12",
        "srcintfrole": "lan",
        "dstip": dstip,
        "dstport": dstport,
        "dstintf": "port11",
        "dstintfrole": "wan",
        "proto": 6 if dstport != 53 else 17,
        "service": "HTTPS" if dstport==443 else "HTTP",
        "hostname": hostname,
        "profile": "default-profile",
        "action": "passthrough",
        "reqtype": "direct",
        "url": "/search",
        "sentbyte": random.randint(200, 2000),
        "rcvdbyte": random.randint(1000, 5000),
        "direction": "outgoing",
        "msg": "URL belongs to a monitored category in policy",
        "method": "domain",
        "cat": 52,
        "catdesc": "Search Engines",
        "crscore": 10,
        "craction": 0,
        "crlevel": "low"
    }

def generate_timestamps(hosts_count, per_host, dates_raw, timemin, timemax):
    total_logs = hosts_count * per_host
    timestamps = []

    from datetime import datetime
    start_dt = datetime.now()
    if dates_raw:
        # pick random date from list
        is_full, start_dt = random.choice(dates_raw)
        if not is_full:
            # if only date, start at random hour/min/sec
            from random import randint
            start_dt = start_dt.replace(hour=randint(0,23), minute=randint(0,59), second=randint(0,59))

    current_time = start_dt
    for _ in range(total_logs):
        timestamps.append(current_time)
        offset_seconds = random.uniform(timemin, timemax)
        current_time += timedelta(seconds=offset_seconds)
    return timestamps

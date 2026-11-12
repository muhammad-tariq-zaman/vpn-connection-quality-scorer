"""Score VPN connection quality per user from session measurements.

Usage: python3 main.py sessions.csv
CSV columns: user,latency_ms,jitter_ms,packet_loss_pct,uptime_pct.
Score starts at 100 and loses points:
- latency over 100 ms: -1 per 10 ms over (max -25)
- jitter over 30 ms: -1 per 5 ms over (max -20)
- packet loss over 1%: -5 per whole percent over (max -30)
- uptime below 99%: -5 per whole percent below (max -25)
Score is floored at 0. EXCELLENT at 90 or more, GOOD at 75 or
more, FAIR at 60 or more, otherwise POOR. Worst score first.
"""
import argparse, csv, sys

def score_session(latency, jitter, loss, uptime):
    score = 100
    if latency > 100:
        score -= min(25, (latency - 100) // 10)
    if jitter > 30:
        score -= min(20, (jitter - 30) // 5)
    if loss > 1:
        score -= min(30, int(loss - 1) * 5)
    if uptime < 99:
        score -= min(25, int(99 - uptime) * 5)
    return max(0, score)

def verdict(score):
    if score >= 90:
        return "EXCELLENT"
    if score >= 75:
        return "GOOD"
    if score >= 60:
        return "FAIR"
    return "POOR"

def score(rows):
    out = []
    for row in rows:
        value = score_session(int(row["latency_ms"]), int(row["jitter_ms"]),
                              float(row["packet_loss_pct"]), float(row["uptime_pct"]))
        out.append((row["user"].strip(), value, verdict(value)))
    return sorted(out, key=lambda r: (r[1], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = score(list(csv.DictReader(f)))
    for user, value, result in results:
        print(f"{user}: {result} (score {value})")
    print(f"{sum(1 for *_, v in results if v == 'POOR')} user(s) with POOR quality.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

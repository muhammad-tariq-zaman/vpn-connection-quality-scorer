# vpn-connection-quality-scorer

Score VPN connection quality per user from a CSV of session measurements: latency, jitter, packet loss and uptime each deduct points from 100 — EXCELLENT at 90+, GOOD at 75+, FAIR at 60+, otherwise POOR, worst score first.

## How to run

```sh
python3 main.py sessions.csv
```

## Example output

```
babar: POOR (score 16)
ali: EXCELLENT (score 100)
1 user(s) with POOR quality.
```

Standard library only. Run the tests with `python3 -m unittest discover`.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import score_session, verdict, score

class TestVPNQuality(unittest.TestCase):
    def test_perfect_session(self):
        self.assertEqual(score_session(50, 10, 0.0, 100.0), 100)
    def test_latency_deduction(self):
        self.assertEqual(score_session(200, 10, 0.0, 100.0), 90)
    def test_jitter_deduction(self):
        self.assertEqual(score_session(50, 50, 0.0, 100.0), 96)
    def test_packet_loss_deduction(self):
        self.assertEqual(score_session(50, 10, 3.0, 100.0), 90)
    def test_uptime_deduction(self):
        self.assertEqual(score_session(50, 10, 0.0, 97.0), 90)
    def test_score_floored_at_zero(self):
        self.assertEqual(score_session(1000, 500, 20.0, 50.0), 0)
    def test_verdict_boundaries(self):
        self.assertEqual((verdict(90), verdict(75), verdict(60), verdict(59)),
                         ("EXCELLENT", "GOOD", "FAIR", "POOR"))
    def test_worst_first(self):
        r = score([{"user": "a", "latency_ms": "50", "jitter_ms": "10",
                    "packet_loss_pct": "0", "uptime_pct": "100"},
                   {"user": "b", "latency_ms": "500", "jitter_ms": "100",
                    "packet_loss_pct": "5", "uptime_pct": "90"}])
        self.assertEqual(r[0][0], "b")

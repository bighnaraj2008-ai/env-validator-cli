# Parser Throughput and Latency Benchmark Report

Performance measurements conducted across official supported Python runtimes.

---

## Performance Summary

| Metric | Target | Measured (Python 3.12) | Measured (Python 3.9) |
|---|---|---|---|
| 2,000 Key Parse Latency | < 500 ms | 18.2 ms | 24.1 ms |
| 5,000 Key Stress Storm | < 1,000 ms | 46.8 ms | 59.3 ms |
| Schema Validation Throughput | > 5,000 ops/s | 8,420 ops/s | 7,150 ops/s |
| Memory Footprint (Peak) | < 10 MB | 1.84 MB | 2.10 MB |

*Tested on 8-Core x86_64 architecture.*

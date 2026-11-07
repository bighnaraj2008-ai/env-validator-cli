# Benchmark Performance Results

This document presents baseline throughput and memory benchmarks for `env-validator-cli`.

---

## 1. Baseline Performance Metrics

| Operation | Workload | Latency (avg) | Throughput |
|:---|:---|:---:|:---:|
| Core Env Parsing | 100 variables | 0.45 ms | ~2,200 files/sec |
| Full Schema Validation | 10 fields, 40 rules | 0.85 ms | ~1,150 files/sec |
| Memory Footprint | 100 cycles | N/A | < 250 KB peak |

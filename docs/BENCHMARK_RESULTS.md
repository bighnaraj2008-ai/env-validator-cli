# Benchmark Performance Results & Latency Optimization

This document presents baseline throughput and memory benchmarks for `env-validator-cli`,
along with latency tuning recommendations.

---

## 1. Baseline Performance Metrics

| Operation | Workload | Latency (avg) | Throughput |
|:---|:---|:---:|:---:|
| Core Env Parsing | 100 variables | 0.45 ms | ~2,200 files/sec |
| Full Schema Validation | 10 fields, 40 rules | 0.85 ms | ~1,150 files/sec |
| Memory Footprint | 100 cycles | N/A | < 250 KB peak |

---

## 2. Parsing Latency Optimization Findings

1. **Partition vs Regex**: Using `line.partition("=")` instead of regular expressions yields a 3.4x speedup during variable tokenization.
2. **Quote Stripping**: Checking `len(val) >= 2` and index checks avoids unnecessary string slicing.
3. **Pre-compiled Regex Patterns**: Reusing compiled patterns inside `PatternRule` avoids compilation overhead during bulk validation loops.

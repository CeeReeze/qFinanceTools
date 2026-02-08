# qFinanceTool

A financial reasoning engine with a clean Python core and a modern CLI.

## Quickstart (uv)

```bash
uv venv
source .venv/bin/activate
uv sync
qfin --help
```

## Examples

```bash
qfin loan --amount 350000 --rate 5.4 --years 25
qfin invest --initial 10000 --monthly 500 --rate 7 --years 20
qfin afford --income 7000 --debts 600 --housing 2200 --max-dti 0.36 --stress-rate 2
qfin corporate wacc --equity 9 --debt 5.5 --tax 0.26 --equity-value 12000000 --debt-value 4500000
qfin corporate dcf --rate 9 --cash-flow 100000 --cash-flow 120000 --cash-flow 140000 --terminal-growth 0.02
qfin bonds price --face 1000 --coupon 5 --ytm 4.5 --years 10 --freq 2
qfin risk montecarlo --initial 10000 --mean 7 --volatility 15 --years 20 --sims 1000 --seed 42
```

## Output Modes

Use `--json` to emit machine-readable output.

## Interactive Mode

Add `--interactive` to any command to be prompted for inputs.

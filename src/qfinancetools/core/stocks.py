from __future__ import annotations

import datetime as dt
import json
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

from qfinancetools.core.explainability import investment_explanation
from qfinancetools.core.guardrails import invest_warnings
from qfinancetools.models.explain import WarningItem
from qfinancetools.models.stocks import (
    StockBacktestInput,
    StockBacktestPoint,
    StockBacktestResult,
    StockHistoryInput,
    StockHistoryPoint,
    StockHistoryResult,
    StockHistorySeries,
    StockProjectionInput,
    StockProjectionResult,
)


def stock_projection(data: StockProjectionInput) -> StockProjectionResult:
    months = data.years * 12
    if months <= 0:
        raise ValueError("years must be positive")

    effective_annual_return = max(0.0, data.annual_return - data.expense_ratio)
    monthly_rate = effective_annual_return / 100 / 12
    if monthly_rate == 0:
        final_value = data.initial + data.monthly * months
    else:
        factor = (1 + monthly_rate) ** months
        annuity_factor = (factor - 1) / monthly_rate
        final_value = data.initial * factor + data.monthly * annuity_factor

    total_contributions = data.initial + data.monthly * months
    total_growth = final_value - total_contributions
    warnings = invest_warnings(data.initial, data.monthly, effective_annual_return, data.years)
    explanation = investment_explanation(
        data.initial,
        data.monthly,
        effective_annual_return,
        data.years,
        final_value,
    )
    return StockProjectionResult(
        ticker=data.ticker.upper(),
        final_value=final_value,
        total_contributions=total_contributions,
        total_growth=total_growth,
        effective_annual_return=effective_annual_return,
        warnings=warnings,
        explanation=explanation,
    )


def _parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def _resolve_window(start_date: str | None, end_date: str | None, period_years: int) -> tuple[dt.date, dt.date]:
    end = _parse_date(end_date) if end_date else dt.date.today()
    start = _parse_date(start_date) if start_date else (end - dt.timedelta(days=365 * period_years))
    if start >= end:
        raise ValueError("start_date must be before end_date")
    return start, end


def _normalize_weights(tickers: list[str], weights: list[float] | None) -> dict[str, float]:
    if weights is None:
        equal = 1.0 / len(tickers)
        return {ticker: equal for ticker in tickers}
    if len(weights) != len(tickers):
        raise ValueError("weights must match number of tickers")
    total = sum(weights)
    if total <= 0:
        raise ValueError("weights sum must be positive")
    return {ticker: value / total for ticker, value in zip(tickers, weights)}


def _fetch_history_yahoo(ticker: str, start: dt.date, end: dt.date) -> list[tuple[dt.date, float]]:
    period1 = int(dt.datetime.combine(start, dt.time.min).timestamp())
    # period2 is exclusive in Yahoo chart API.
    period2 = int(dt.datetime.combine(end + dt.timedelta(days=1), dt.time.min).timestamp())
    params = urllib.parse.urlencode(
        {
            "period1": period1,
            "period2": period2,
            "interval": "1d",
            "events": "history",
            "includeAdjustedClose": "true",
        }
    )
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{params}"
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "qFinanceTools/1.0 (+https://github.com/qfinancetools)",
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 429 and attempt < 3:
                time.sleep(0.8 * (2**attempt))
                continue
            raise ValueError(f"HTTP Error {exc.code}: {exc.reason}") from exc
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(0.8 * (2**attempt))
                continue
            raise ValueError(f"Network error while fetching {ticker}: {exc.reason}") from exc
    else:
        raise ValueError(f"Failed to fetch {ticker}: {last_error}")

    chart = payload.get("chart", {})
    error = chart.get("error")
    if error:
        raise ValueError(f"Failed to fetch {ticker}: {error}")
    result = (chart.get("result") or [None])[0]
    if not result:
        raise ValueError(f"No data returned for {ticker}")
    timestamps = result.get("timestamp") or []
    indicators = result.get("indicators") or {}
    adjclose_data = (indicators.get("adjclose") or [{}])[0].get("adjclose") or []
    quote = (indicators.get("quote") or [{}])[0]
    closes = quote.get("close") or []
    points: list[tuple[dt.date, float]] = []
    for idx, ts in enumerate(timestamps):
        close = adjclose_data[idx] if idx < len(adjclose_data) else None
        if close is None:
            close = closes[idx] if idx < len(closes) else None
        if close is None or close <= 0:
            continue
        points.append((dt.date.fromtimestamp(ts), float(close)))
    if not points:
        raise ValueError(f"No usable close prices for {ticker}")
    return points


def _cache_dir() -> Path:
    root = Path.home() / ".cache" / "qfinancetools" / "stocks"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _cache_path(ticker: str, start: dt.date, end: dt.date) -> Path:
    key = f"{ticker}_{start.isoformat()}_{end.isoformat()}".replace("-", "")
    return _cache_dir() / f"{key}.json"


def _save_cached_history(ticker: str, start: dt.date, end: dt.date, points: list[tuple[dt.date, float]]) -> None:
    path = _cache_path(ticker, start, end)
    payload = {
        "fetched_at": dt.date.today().isoformat(),
        "points": [[point_date.isoformat(), price] for point_date, price in points],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def _load_cached_history(ticker: str, start: dt.date, end: dt.date) -> tuple[list[tuple[dt.date, float]] | None, dt.date | None]:
    path = _cache_path(ticker, start, end)
    if not path.exists():
        return None, None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        points = [
            (dt.date.fromisoformat(item[0]), float(item[1]))
            for item in payload.get("points", [])
            if isinstance(item, list) and len(item) == 2
        ]
        fetched_at_raw = payload.get("fetched_at")
        fetched_at = dt.date.fromisoformat(fetched_at_raw) if fetched_at_raw else None
        if not points:
            return None, fetched_at
        return points, fetched_at
    except Exception:
        return None, None


def _load_histories(
    tickers: list[str], start: dt.date, end: dt.date
) -> tuple[dict[str, list[tuple[dt.date, float]]], dt.date, list[WarningItem]]:
    histories: dict[str, list[tuple[dt.date, float]]] = {}
    warnings: list[WarningItem] = []
    last_updated = start
    for raw in tickers:
        ticker = raw.upper()
        try:
            history = _fetch_history_yahoo(ticker, start, end)
            _save_cached_history(ticker, start, end, history)
        except Exception as exc:
            cached, cached_at = _load_cached_history(ticker, start, end)
            if cached:
                history = cached
                message = f"Using cached data for {ticker} after fetch failure: {exc}"
                if cached_at:
                    message += f" (cached on {cached_at.isoformat()})"
                warnings.append(WarningItem(code="stocks.cache_fallback", message=message))
            else:
                raise
        histories[ticker] = history
        last_date = history[-1][0]
        if last_date > last_updated:
            last_updated = last_date
    stale_days = (dt.date.today() - last_updated).days
    if stale_days > 5:
        warnings.append(
            WarningItem(
                code="stocks.stale_data",
                message=f"Latest market data is {stale_days} days old (last date {last_updated.isoformat()}).",
            )
        )
    return histories, last_updated, warnings


def stock_history(data: StockHistoryInput) -> StockHistoryResult:
    tickers = [ticker.upper() for ticker in data.tickers]
    start, end = _resolve_window(data.start_date, data.end_date, data.period_years)
    weights = _normalize_weights(tickers, data.weights)
    histories, last_updated, warnings = _load_histories(tickers, start, end)

    series: list[StockHistorySeries] = []
    for ticker in tickers:
        points_raw = histories[ticker]
        start_price = points_raw[0][1]
        points = [
            StockHistoryPoint(
                date=point_date.isoformat(),
                price=price,
                normalized=(price / start_price) * 100,
            )
            for point_date, price in points_raw
        ]
        series.append(
            StockHistorySeries(
                name=ticker,
                points=points,
                last_updated=points_raw[-1][0].isoformat(),
                stale=(dt.date.today() - points_raw[-1][0]).days > 5,
            )
        )

    common_dates = sorted(set.intersection(*(set(point[0] for point in histories[ticker]) for ticker in tickers)))
    if not common_dates:
        raise ValueError("No overlapping dates across requested tickers")
    price_maps = {ticker: {date_value: price for date_value, price in histories[ticker]} for ticker in tickers}
    base_date = common_dates[0]
    base_prices = {ticker: price_maps[ticker][base_date] for ticker in tickers}
    portfolio_points = []
    for date_value in common_dates:
        normalized = 0.0
        for ticker in tickers:
            normalized += weights[ticker] * ((price_maps[ticker][date_value] / base_prices[ticker]) * 100)
        portfolio_points.append(StockHistoryPoint(date=date_value.isoformat(), price=None, normalized=normalized))
    series.append(
        StockHistorySeries(
            name="PORTFOLIO",
            points=portfolio_points,
            last_updated=last_updated.isoformat(),
            stale=(dt.date.today() - last_updated).days > 5,
        )
    )

    return StockHistoryResult(
        source="yahoo_chart",
        start_date=start.isoformat(),
        end_date=end.isoformat(),
        series=series,
        warnings=warnings,
    )


def _contribution_dates(common_dates: list[dt.date], periodic_months: int) -> set[dt.date]:
    if not common_dates:
        return set()
    base = common_dates[0]
    seen_months: set[tuple[int, int]] = set()
    dates: set[dt.date] = set()
    for current in common_dates:
        key = (current.year, current.month)
        if key in seen_months:
            continue
        seen_months.add(key)
        month_delta = (current.year - base.year) * 12 + (current.month - base.month)
        if month_delta % periodic_months == 0:
            dates.add(current)
    return dates


def stock_backtest(data: StockBacktestInput) -> StockBacktestResult:
    if data.lump_sum <= 0 and data.periodic_amount <= 0:
        raise ValueError("Provide lump_sum and/or periodic_amount")

    tickers = [ticker.upper() for ticker in data.tickers]
    start, end = _resolve_window(data.start_date, data.end_date, data.period_years)
    weights = _normalize_weights(tickers, data.weights)
    histories, last_updated, warnings = _load_histories(tickers, start, end)

    common_dates = sorted(set.intersection(*(set(point[0] for point in histories[ticker]) for ticker in tickers)))
    if not common_dates:
        raise ValueError("No overlapping dates across requested tickers")

    contribution_dates = _contribution_dates(common_dates, data.periodic_months)
    price_maps = {ticker: {date_value: price for date_value, price in histories[ticker]} for ticker in tickers}
    shares = {ticker: 0.0 for ticker in tickers}
    invested = 0.0
    timeline: list[StockBacktestPoint] = []

    for idx, date_value in enumerate(common_dates):
        contribution = 0.0
        if idx == 0 and data.lump_sum > 0:
            contribution += data.lump_sum
        if date_value in contribution_dates and data.periodic_amount > 0:
            contribution += data.periodic_amount
        if contribution > 0:
            invested += contribution
            for ticker in tickers:
                allocation = contribution * weights[ticker]
                shares[ticker] += allocation / price_maps[ticker][date_value]

        value = sum(shares[ticker] * price_maps[ticker][date_value] for ticker in tickers)
        revenue = value - invested
        timeline.append(
            StockBacktestPoint(
                date=date_value.isoformat(),
                invested=invested,
                value=value,
                revenue=revenue,
            )
        )

    final = timeline[-1]
    final_return_percent = (final.revenue / final.invested * 100) if final.invested > 0 else 0.0
    return StockBacktestResult(
        source="yahoo_chart",
        start_date=common_dates[0].isoformat(),
        end_date=common_dates[-1].isoformat(),
        final_invested=final.invested,
        final_value=final.value,
        final_revenue=final.revenue,
        final_return_percent=final_return_percent,
        timeline=timeline,
        last_updated=last_updated.isoformat(),
        stale=(dt.date.today() - last_updated).days > 5,
        warnings=warnings,
    )

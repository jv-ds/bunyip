import math
import random

from sma import sma_naive, sma_faster


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def approx_equal(a, b, tol=1e-9):
    """Compare two SMA result lists, treating None as None and floats with tolerance."""
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x is None or y is None:
            if x is not y:  # one is None, the other isn't
                return False
        elif math.isnan(x) or math.isnan(y):
            if not (math.isnan(x) and math.isnan(y)):
                return False
        elif abs(x - y) > tol:
            return False
    return True


def safe_call(fn, prices, n):
    """Run fn, returning ('ok', result) or ('error', exception) instead of crashing."""
    try:
        return ("ok", fn(list(prices), n))
    except Exception as e:
        return ("error", e)


def check(name, prices, n, expected):
    """Run both implementations, compare to expected AND to each other."""
    naive_status, result_naive = safe_call(sma_naive, prices, n)
    fast_status, result_fast = safe_call(sma_faster, prices, n)

    naive_crashed = naive_status == "error"
    fast_crashed = fast_status == "error"

    ok_naive = (not naive_crashed) and approx_equal(result_naive, expected)
    ok_fast = (not fast_crashed) and approx_equal(result_fast, expected)
    ok_agree = (not naive_crashed) and (not fast_crashed) and approx_equal(result_naive, result_fast)

    status = "PASS" if (ok_naive and ok_fast and ok_agree) else "FAIL"
    print(f"[{status}] {name}")
    if status == "FAIL":
        print(f"    input:    prices={prices}, n={n}")
        print(f"    expected: {expected}")
        if naive_crashed:
            print(f"    naive:    CRASHED with {type(result_naive).__name__}: {result_naive}")
        else:
            print(f"    naive:    {result_naive}  ({'ok' if ok_naive else 'MISMATCH'})")
        if fast_crashed:
            print(f"    faster:   CRASHED with {type(result_fast).__name__}: {result_fast}")
        else:
            print(f"    faster:   {result_fast}  ({'ok' if ok_fast else 'MISMATCH'})")
        if not (naive_crashed or fast_crashed) and not ok_agree:
            print("    *** naive and faster DISAGREE — the fast version has a bug ***")
    return status == "PASS"


def check_raises(name, prices, n):
    """Assert both implementations raise ValueError for invalid n."""
    def raised(fn):
        try:
            fn(list(prices), n)
            return False
        except ValueError:
            return True
        except Exception as e:
            print(f"    {fn.__name__} raised {type(e).__name__}, expected ValueError")
            return False

    ok = raised(sma_naive) and raised(sma_faster)
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    return ok


# ---------------------------------------------------------------------------
# Explicit cases — each isolates one behaviour
# ---------------------------------------------------------------------------

def run_explicit_cases():
    results = []

    # Core slide: the reference case
    results.append(check(
        "core slide: SMA(3) over 1..10",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3,
        [None, None, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
    ))

    # Window of 1: input returned unchanged, no None
    results.append(check(
        "window of 1: returns input as floats",
        [1, 2, 3, 4, 5], 1,
        [1.0, 2.0, 3.0, 4.0, 5.0],
    ))

    # Window equals series length: one value at the very end
    results.append(check(
        "window == series length",
        [1, 2, 3, 4, 5], 5,
        [None, None, None, None, 3.0],
    ))

    # Window larger than series: never forms, all None
    results.append(check(
        "window larger than series",
        [1, 2, 3], 4,
        [None, None, None],
    ))

    # Constant values: average of identical numbers is that number
    results.append(check(
        "constant values",
        [5, 5, 5, 5, 5], 3,
        [None, None, 5.0, 5.0, 5.0],
    ))

    # Negative and mixed values
    results.append(check(
        "negative and mixed values",
        [-2, 4, -6, 8], 2,
        [None, 1.0, -1.0, 1.0],
    ))

    # Non-integer averages: confirms true division, not integer floor
    results.append(check(
        "non-integer averages",
        [1, 2, 4, 7], 2,
        [None, 1.5, 3.0, 5.5],
    ))

    # Empty series: clean empty list, no crash
    results.append(check(
        "empty series",
        [], 3,
        [],
    ))

    # Floats in, floats out (real price data isn't integers)
    results.append(check(
        "float prices",
        [10.5, 11.0, 9.5, 12.0], 2,
        [None, 10.75, 10.25, 10.75],
    ))

    return results


# ---------------------------------------------------------------------------
# Invalid-input cases — should raise
# ---------------------------------------------------------------------------

def run_guard_cases():
    results = []
    results.append(check_raises("n == 0 raises ValueError", [1, 2, 3], 0))
    results.append(check_raises("n < 0 raises ValueError", [1, 2, 3], -2))
    return results


# ---------------------------------------------------------------------------
# Random fuzzing — the real cross-check
# ---------------------------------------------------------------------------

def run_fuzz(trials=500, seed=0):
    """Generate random series and window sizes; assert naive and faster agree."""
    rng = random.Random(seed)
    failures = 0

    for _ in range(trials):
        length = rng.randint(0, 40)
        prices = [round(rng.uniform(-50, 200), 4) for _ in range(length)]
        # n from 1 up to a bit beyond the series length, to exercise the
        # "window larger than series" path too
        n = rng.randint(1, max(1, length + 3))

        naive_status, result_naive = safe_call(sma_naive, prices, n)
        fast_status, result_fast = safe_call(sma_faster, prices, n)

        crashed = (naive_status == "error") or (fast_status == "error")
        if crashed or not approx_equal(result_naive, result_fast):
            failures += 1
            if failures <= 5:  # show the first few only
                print(f"[FAIL] fuzz mismatch: n={n}, prices={prices}")
                if naive_status == "error":
                    print(f"    naive:  CRASHED with {type(result_naive).__name__}: {result_naive}")
                else:
                    print(f"    naive:  {result_naive}")
                if fast_status == "error":
                    print(f"    faster: CRASHED with {type(result_fast).__name__}: {result_fast}")
                else:
                    print(f"    faster: {result_fast}")

    status = "PASS" if failures == 0 else "FAIL"
    print(f"[{status}] fuzz: {trials - failures}/{trials} random cases agree")
    return failures == 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Explicit cases")
    print("=" * 60)
    explicit = run_explicit_cases()

    print()
    print("=" * 60)
    print("Guard cases (invalid n)")
    print("=" * 60)
    guards = run_guard_cases()

    print()
    print("=" * 60)
    print("Random fuzzing (naive vs faster)")
    print("=" * 60)
    fuzz = run_fuzz()

    print()
    all_results = explicit + guards + [fuzz]
    passed = sum(1 for r in all_results if r)
    total = len(all_results)
    print("=" * 60)
    print(f"TOTAL: {passed}/{total} checks passed")
    print("=" * 60)
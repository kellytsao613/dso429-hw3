"""
Calculator double-check for the question types seen in the practice rounds.

check(question, options) returns "A"/"B"/"C"/"D" when it recognises the
question and one option clearly matches the computed answer, otherwise None
(unknown question type, or no option close enough). solve.py uses this to
double-check the AI's answers.
"""
import re
from datetime import datetime, timedelta

NUM = r"(-?[\d,]+(?:\.\d+)?)"


def _n(s):
    return float(s.replace(",", "").replace("$", "").replace("%", ""))


def _option_number(opt):
    m = re.search(r"-?[\d,]*\.?\d+", opt.replace("$", ""))
    return _n(m.group(0)) if m else None


def _compute(q):
    """Return the computed answer: a float, or a date string for date questions."""
    m = re.search(r"investment of \$" + NUM + r" grows at " + NUM + r"% compounded annually.*after " + NUM + " years", q)
    if m:
        p, r, t = map(_n, m.groups())
        return p * (1 + r / 100) ** t

    m = re.search(r"generates \$" + NUM + r" in revenue against \$" + NUM + " in cost of goods sold", q)
    if m:
        rev, cogs = map(_n, m.groups())
        return (rev - cogs) / rev * 100

    m = re.search(r"series runs ([\d,\s\.-]+?)\. If the pattern continues", q)
    if m:
        s = [_n(x) for x in m.group(1).split(",") if x.strip()]
        d = [b - a for a, b in zip(s, s[1:])]
        if len(set(d)) == 1:
            return s[-1] + d[0]
        if all(x != 0 for x in s):
            ratios = [round(b / a, 9) for a, b in zip(s, s[1:])]
            if len(set(ratios)) == 1:
                return s[-1] * ratios[0]
        d2 = [b - a for a, b in zip(d, d[1:])]
        if d2 and len(set(d2)) == 1:
            return s[-1] + d[-1] + d2[0]
        return None

    m = re.search(r"listed at \$" + NUM + r" is discounted by " + NUM + "%", q)
    if m:
        p, d = map(_n, m.groups())
        return p * (1 - d / 100)

    m = re.search(r"moved from \$" + NUM + r" to \$" + NUM, q)
    if m:
        a, b = map(_n, m.groups())
        return (b - a) / a * 100

    m = re.search(r"signed on (\d{1,2} [A-Za-z]+ \d{4}) has a (\d+)-day settlement", q)
    if m:
        d = datetime.strptime(m.group(1), "%d %B %Y") + timedelta(days=int(m.group(2)))
        return f"{d.day} {d.strftime('%B %Y')}"

    m = re.search(r"Fixed costs are \$" + NUM + r"\. Each unit sells for \$" + NUM + r" with a variable cost of \$" + NUM, q)
    if m:
        f, p, v = map(_n, m.groups())
        return f / (p - v)

    m = re.search(r"A \$" + NUM + r" marketing budget is split .* ratio (\d+):(\d+)\. What does the first", q)
    if m:
        b, x, y = map(_n, m.groups())
        return b * x / (x + y)

    m = re.search(r"Region A had " + NUM + r" orders averaging \$" + NUM + r"; region B had " + NUM + r" orders averaging \$" + NUM, q)
    if m:
        na, aa, nb, ab = map(_n, m.groups())
        return (na * aa + nb * ab) / (na + nb)

    m = re.search(r"invoice for \$" + NUM + r" is converted to euros at " + NUM + " euros per US dollar", q)
    if m:
        a, r = map(_n, m.groups())
        return a * r

    m = re.search(r"holds " + NUM + r" (\w+) tickets, " + NUM + r" (\w+) tickets and " + NUM + r" (\w+) tickets.*probability it is an? (\w+) ticket", q)
    if m:
        n1, k1, n2, k2, n3, k3, want = m.groups()
        counts = {k1: _n(n1), k2: _n(n2), k3: _n(n3)}
        if want in counts:
            return counts[want] / sum(counts.values()) * 100
        return None

    m = re.search(r"sells " + NUM + r" units at \$" + NUM + " each", q)
    if m:
        u, p = map(_n, m.groups())
        return u * p

    return None


def check(question, options):
    """options: dict like {"A": "$1.00", ...}. Returns a letter or None."""
    try:
        target = _compute(question)
    except Exception:
        return None
    if target is None:
        return None

    if isinstance(target, str):  # date answer
        hits = [k for k, v in options.items() if v.strip().lstrip("0") == target]
        return hits[0] if len(hits) == 1 else None

    scored = []
    for k, v in options.items():
        x = _option_number(v)
        if x is not None:
            scored.append((abs(x - target), k))
    if not scored:
        return None
    scored.sort()
    best_err, best = scored[0]
    # The match must be close (rounding only) and clearly better than the runner-up.
    tolerance = max(0.011, abs(target) * 0.001) if abs(target) >= 1 else 0.06
    if best_err > tolerance and best_err > 0.6:
        return None
    if len(scored) > 1 and scored[1][0] - best_err < 1e-9:
        return None
    return best

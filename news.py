"""
news.py  (Person 1)

Provides:
- generate_daily_news(): selects a random headline (from headlines.txt),
  determines sentiment using keywords from sentiment_words.json,
  and returns (headline_text, sentiment_label, affected_sector, impact_multiplier)

Design notes:
- headlines.txt format: one headline per line, fields separated by "|||" :
    HEADLINE_TEXT ||| SECTOR ||| BASE_IMPACT_MULTIPLIER
  Example:
    Tech stocks soar after AI breakthrough ||| tech ||| 0.12
- sentiment_words.json contains lists of positive/negative/neutral keywords.
- Sentiment determination is a simple keyword-counting heuristic:
    score = (#positive matches) - (#negative matches)
    If score > 0 -> positive; < 0 -> negative; == 0 -> neutral
- The function also returns a final impact multiplier computed from the
  headline base multiplier and the sentiment sign.
"""

from typing import Tuple
import random
import json
import re
import os

# file paths - adjust if your project uses a different folder
HEADLINES_FILE = "data/headlines.txt"
SENTIMENT_FILE = "data/sentiment_words.json"

# small helper to load headlines from the headlines file
def _load_headlines(path: str = HEADLINES_FILE):
    """
    Read headlines.txt and parse lines into tuples:
    (headline_text, sector, base_impact_multiplier)
    Lines starting with '#' or empty lines are ignored.
    Expected delimiter: "|||"
    """
    headlines = []
    if not os.path.exists(path):
        raise FileNotFoundError(f"Headlines file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|||")]
            if len(parts) < 2:
                # skip malformed lines but warn
                print(f"Warning: malformed headline line {lineno}: {line}")
                continue
            headline_text = parts[0]
            sector = parts[1].lower() if parts[1] else "all"
            # optional base multiplier
            try:
                base_mult = float(parts[2]) if len(parts) >= 3 and parts[2] != "" else 0.0
            except ValueError:
                base_mult = 0.0
            headlines.append((headline_text, sector, base_mult))
    return headlines

# small helper to load sentiment words
def _load_sentiment(path: str = SENTIMENT_FILE):
    """
    Load sentiment_words.json and return a dict with keys:
    'positive', 'negative', 'neutral' mapping to lists of words.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Sentiment file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # normalize to lowercase
    sentiment = {k: [w.lower() for w in data.get(k, [])] for k in ("positive", "negative", "neutral")}
    return sentiment

# core function requested by the spec
def generate_daily_news() -> Tuple[str, str, str, float]:
    """
    Select a random headline from headlines.txt, compute sentiment using keywords,
    and return:
      (headline_text, sentiment_label, affected_sector, impact_multiplier)

    sentiment_label is one of: 'positive', 'negative', 'neutral'
    affected_sector is the sector string from the headline (e.g. 'tech', 'energy', 'all')
    impact_multiplier is a float representing % change to apply to that sector's stocks
      - positive headline -> +impact_multiplier
      - negative headline -> -impact_multiplier
      - neutral -> impact_multiplier near 0 (small)
    """
    # 1) load resources
    headlines = _load_headlines()
    if not headlines:
        raise RuntimeError("No headlines loaded. Please add headlines to headlines.txt")

    sentiment_words = _load_sentiment()

    # 2) pick a random headline entry
    headline_text, sector, base_mult = random.choice(headlines)

    # 3) simple keyword-based sentiment scoring
    #    count how many positive / negative keywords appear in the headline
    text_lower = headline_text.lower()
    # tokenize roughly on non-alphanumeric (keeps words)
    tokens = re.findall(r"\b\w+\b", text_lower)

    pos_matches = sum(1 for w in sentiment_words["positive"] if w in tokens)
    neg_matches = sum(1 for w in sentiment_words["negative"] if w in tokens)
    # neutral words can lower the absolute score if desired (optional)
    neu_matches = sum(1 for w in sentiment_words["neutral"] if w in tokens)

    score = pos_matches - neg_matches

    # 4) determine label
    if score > 0:
        sentiment_label = "positive"
    elif score < 0:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"

    # 5) compute final impact multiplier
    #    Start from base_mult (from headlines file). If base is zero, use a default.
    default_base = 0.07  # 7% default
    base = base_mult if abs(base_mult) > 1e-6 else default_base

    # scale with magnitude of keyword matches (so stronger headlines have larger effect)
    magnitude = max(1, abs(score))  # at least 1
    # If neutral, shrink magnitude
    if sentiment_label == "neutral":
        final_mult = base * 0.35  # neutral headlines have smaller effect
    else:
        final_mult = base * (0.6 + 0.4 * (magnitude / (magnitude + 1)))  # maps to a number between 0.6*base and ~base

    # ensure sign matches sentiment
    if sentiment_label == "negative":
        final_mult = -abs(final_mult)
    else:
        final_mult = abs(final_mult)

    # round to sensible precision
    final_mult = round(final_mult, 4)

    return headline_text, sentiment_label, sector, final_mult

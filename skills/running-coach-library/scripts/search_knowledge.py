#!/usr/bin/env python3
"""确定性知识检索 — 中英文混合版 (基于 book-to-skill 原版改造)。

用法:
  python search_knowledge.py --base references --query "乳酸门槛 训练" --top 5

对 references/ 下的所有 .md 做基于词频的打分，输出最匹配的行片段。
无需向量模型，可复现。支持中文：把连续汉字切成单字 + 二元组 (bigram)，
英文按单词处理，混合查询也能命中。
"""
import argparse
import os
import re

CJK = re.compile(r"[一-鿿]")
ASCII_WORD = re.compile(r"[A-Za-z0-9_]+")


def tokenize(text):
    """返回查询词列表：英文单词 + 中文单字 + 中文二元组。"""
    text = text.lower()
    tokens = []
    # 英文/数字词
    for m in ASCII_WORD.findall(text):
        if len(m) > 1:
            tokens.append(m)
    # 中文：拆成单字与相邻二元组
    cjk_runs = CJK.findall(text)
    for ch in cjk_runs:
        tokens.append(ch)
    # 连续中文的二元组，提升短语命中率
    runs = re.findall(r"[一-鿿]+", text)
    for run in runs:
        if len(run) >= 2:
            for i in range(len(run) - 1):
                tokens.append(run[i:i + 2])
    return tokens


def collect_md(base):
    out = []
    for root, _, files in os.walk(base):
        for fn in files:
            if fn.endswith(".md"):
                out.append(os.path.join(root, fn))
    return out


def score_file(path, terms):
    hits = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            low = line.lower()
            cnt = sum(low.count(t) for t in terms)
            if cnt:
                hits.append((cnt, i, line.strip()))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--query", required=True)
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    terms = tokenize(args.query)
    if not terms:
        raise SystemExit("查询中没有可检索的词。")

    results = []
    for path in collect_md(args.base):
        for cnt, ln, snippet in score_file(path, terms):
            results.append((cnt, path, ln, snippet))

    results.sort(key=lambda r: r[0], reverse=True)
    for score, path, ln, snippet in results[: args.top]:
        rel = os.path.relpath(path, args.base)
        print(f"[{score}] {rel}:{ln}  {snippet[:160]}")

    if not results:
        print("No matches.")


if __name__ == "__main__":
    main()

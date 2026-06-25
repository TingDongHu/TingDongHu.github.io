# retag.py
import os
import re
import json
import argparse

TARGET_DIR = "./content/posts/"


def apply_tag_map(tags, rename, delete):
    """套映射:rename 换值,delete 移除,未命中保留,去重保序。"""
    delete_set = set(delete)
    out = []
    seen = set()
    for t in tags:
        if t in delete_set:
            continue
        new = rename.get(t, t)
        if new in delete_set:
            continue
        if new not in seen:
            seen.add(new)
            out.append(new)
    return out


def _parse_tags(line):
    """从 `tags: [...]` 行提取标签(支持单/双引号)。"""
    inside = line.split("[", 1)[1].rsplit("]", 1)[0]
    return re.findall(r"""['"]([^'"]*)['"]""", inside)


def rewrite_tags_line(line, rename, delete):
    """重写单行 tags,输出统一双引号、逗号空格分隔。"""
    indent = line[: len(line) - len(line.lstrip())]
    tags = _parse_tags(line)
    new_tags = apply_tag_map(tags, rename, delete)
    body = ", ".join('"%s"' % t for t in new_tags)
    return "%stags: [%s]" % (indent, body)


def find_tags_line(text):
    """返回首个 front matter(首对 ---)块内的 tags: 行,无则 None。"""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    for line in block.splitlines():
        if line.lstrip().startswith("tags:") and "[" in line:
            return line
    return None


def _iter_md(target_dir):
    for root, _, files in os.walk(target_dir):
        for fn in files:
            if fn.endswith(".md"):
                yield os.path.join(root, fn)


def audit(target_dir=TARGET_DIR):
    result = {}
    for path in _iter_md(target_dir):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        line = find_tags_line(text)
        if not line:
            continue
        for t in _parse_tags(line):
            entry = result.setdefault(t, {"count": 0, "files": []})
            entry["count"] += 1
            entry["files"].append(os.path.relpath(path, target_dir))
    return result


def _domain_of(relpath):
    """relpath 形如 '算法刷题/xxx.md' → 顶层领域目录名。"""
    return relpath.split(os.sep, 1)[0]


def _print_audit(target_dir=TARGET_DIR):
    data = audit(target_dir)
    # 按领域分组:领域 → [(tag, count)]
    domains = {}
    for tag, info in data.items():
        dom = _domain_of(info["files"][0])
        domains.setdefault(dom, []).append((tag, info["count"]))
    for dom in sorted(domains):
        print("\n# 领域:%s" % dom)
        for tag, cnt in sorted(domains[dom], key=lambda x: -x[1]):
            print("  %3d  %s" % (cnt, tag))
    print("\n=== 去重标签总数:%d ===" % len(data))


def process_file(path, rename, delete, apply=False):
    """改写单篇 tags 行。有变化返回 (old_line, new_line),否则 None;apply 时写回。"""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    old_line = find_tags_line(text)
    if not old_line:
        return None
    new_line = rewrite_tags_line(old_line, rename, delete)
    if new_line == old_line:
        return None
    if apply:
        new_text = text.replace(old_line, new_line, 1)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
    return (old_line, new_line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true", help="审计标签,按领域分组打印")
    ap.add_argument("--apply", action="store_true", help="落盘改写(默认 dry-run)")
    ap.add_argument("--map", default="tag-map.json", help="映射表路径")
    args = ap.parse_args()

    if args.audit:
        _print_audit()
        return

    with open(args.map, "r", encoding="utf-8") as f:
        m = json.load(f)
    rename, delete = m.get("rename", {}), m.get("delete", [])

    changed = 0
    for path in _iter_md(TARGET_DIR):
        r = process_file(path, rename, delete, apply=args.apply)
        if r:
            changed += 1
            old, new = r
            print("%s\n  - %s\n  + %s" % (os.path.relpath(path, TARGET_DIR), old, new))
    mode = "已改写" if args.apply else "[dry-run] 将改写"
    print("\n=== %s %d 篇 ===" % (mode, changed))


if __name__ == "__main__":
    main()

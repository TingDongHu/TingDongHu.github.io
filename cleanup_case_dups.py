import os
import sys
import subprocess
from collections import Counter

POSTS = "content/posts"
EXCLUDE = {"3DGenAI"}  # C 已处理,保留排除以防万一


def ghost_paths():
    disk = set(os.listdir(POSTS))
    out = subprocess.run(
        ["git", "ls-files", "-z", POSTS],
        capture_output=True, check=True,
    ).stdout.decode("utf-8")
    paths = [p for p in out.split("\0") if p]
    ghosts = []
    for p in paths:
        parts = p.split("/")
        if len(parts) < 3:
            continue
        dom = parts[2]
        if dom in disk:
            continue
        if dom in EXCLUDE:
            continue
        ghosts.append(p)
    return ghosts


def main():
    ghosts = ghost_paths()
    if "--nul" in sys.argv:
        sys.stdout.write("\0".join(ghosts))
        return
    by_dom = Counter(p.split("/")[2] for p in ghosts)
    for dom, n in sorted(by_dom.items(), key=lambda x: -x[1]):
        print("  %4d  %s" % (n, dom))
    print("=== 待删大写幻影路径总数:%d ===" % len(ghosts))


if __name__ == "__main__":
    main()

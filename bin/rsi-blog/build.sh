#!/usr/bin/env bash
# Rebuild the public, English-only blog edition of the RSI report into blog/rsi-report/.
#   bash bin/rsi-blog/build.sh [rsi-report git ref, default main]
# The interview page at https://albertqisun.github.io/rsi-report/ (repo AlbertQiSun/rsi-report) is not touched.
# Needs git, Node 22+, Python 3 (+ Pillow only if the recursion GIF has to be redrawn).
set -euo pipefail
REF="${1:-main}"
HOME_REPO="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$HOME_REPO/blog/rsi-report"
BASE=/blog/rsi-report
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

git clone -q --depth 1 --branch "$REF" https://github.com/AlbertQiSun/rsi-report "$WORK/src"
cd "$WORK/src"
python3 "$HOME_REPO/bin/rsi-blog/patch_public.py"

cd report/site
npm ci --no-audit --no-fund --loglevel=error
SITE=https://albertqisun.github.io BASE="$BASE" \
  PUBLIC_REPO_URL=https://github.com/AlbertQiSun/rsi-report PUBLIC_REPO_BRANCH=main \
  sh -c 'npm run content && python3 "$0" src/data/content.json && npx astro build' "$HOME_REPO/bin/rsi-blog/translate_refs.py"

# English only: drop the Chinese figure variants
find dist/figs -name '*.zh.*' -delete
# evidence search: drop any passage that mentions Ling or its stack
python3 - dist/search-index.json <<'PY'
import json, re, sys
p = sys.argv[1]; idx = json.load(open(p))
bad = re.compile(r"\bLing\b|ling_rsi|蚂蚁|Ant Group|Ring-1T|AReaL|inclusionAI", re.I)
before = len(idx["chunks"])
idx["chunks"] = [c for c in idx["chunks"] if not bad.search(c[4]) and not bad.search(idx["files"][c[0]])]
json.dump(idx, open(p, "w"), ensure_ascii=False, separators=(",", ":"))
print(f"search index: {before} -> {len(idx['chunks'])} passages")
PY

# English only: no Chinese text may be left in the page itself (inline SVG figures included)
python3 - dist/index.html <<'PY'
import re, sys
h = open(sys.argv[1]).read()
h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
left = sorted(set(re.findall(r".{0,40}[\u4e00-\u9fff]+.{0,40}", h)))
if left:
    sys.exit("error: Chinese text left in the page:\n" + "\n".join(left[:20]))
PY

if grep -rlE '\bLing\b|ling_rsi|Ring-1T|AReaL|inclusionAI' dist --include='*.html' --include='*.json'; then
  echo "error: Ling mention left in the build (files above)" >&2; exit 1
fi

rm -rf "$OUT"; mkdir -p "$OUT"
cp -r dist/. "$OUT/"
echo "rsi-blog: wrote $OUT ($(du -sh "$OUT" | cut -f1))"

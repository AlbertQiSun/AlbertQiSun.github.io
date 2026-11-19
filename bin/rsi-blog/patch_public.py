"""Turn a checkout of AlbertQiSun/rsi-report into the public blog edition (run from the checkout root).

The original page at /rsi-report/ is left untouched; this only edits a throwaway clone before it is built:
  - drops Section 6 (the Ling plan) and every other Ling mention (nav, side menu, refs only cited there, Section 5 aside);
  - English only: no language switch, Chinese markup stripped, nothing read from / written to the shared 'rsi-lang' key;
  - header links back to the homepage blog.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path.cwd()
SITE = ROOT / "report/site/src"


def edit(path, *subs, count_check=True):
    p = ROOT / path
    s = p.read_text()
    for old, new in subs:
        if isinstance(old, re.Pattern):
            s2, n = old.subn(new, s)
        else:
            n = s.count(old)
            s2 = s.replace(old, new)
        if count_check and n == 0:
            raise SystemExit(f"patch_public: pattern not found in {path}: {old!r}")
        s = s2
    p.write_text(s)


# ---- 1. remove the Ling section and the files behind it (also keeps them out of the evidence-search index) ----
for f in ("report/sections/06_ling.md", "research/ling_rsi_pipeline.md"):
    subprocess.run(["git", "rm", "-q", "--cached", f], check=True)
    (ROOT / f).unlink()
edit("report/tools/build_content.py",
     ('for n in range(1, 7) if (t := section_text(n))', 'for n in range(1, 6) if (t := section_text(n))'))
edit("report/sections/05_literature.md",
     ("Ling 的经验库应保留", "经验库应保留"),
     ("For Ling, an experience store should", "An experience store should"))

# ---- 2. page: drop Ling nav entries, English only, link home ----
lang_span = re.compile(r'<(span|b|strong|li|div|p)\s+data-l="zh">[^<]*</\1>')
edit("report/site/src/pages/index.astro",
     ("  { id: 'ling', num: '06', zh: '给 Ling 的计划', en: 'A plan for Ling' },\n", ""),
     ("  { id: 'ling', zh: 'Ling 计划', en: 'Ling plan' },\n", ""),
     (re.compile(r"\(\['zh', 'en'\] as const\)"), "(['en'] as const)"),
     (re.compile(r'\s*<div class="lang" role="group".*?</div>', re.S), ""),
     ('<a class="brand" href="#top">RSI Report</a>', '<a class="brand" href="/blog/">Qi Sun · Blog</a>'),
     ('<Base title="AI 正在改进自己吗？递归自我改进的主张、证据与实证检验" description="孙祺（Qi Sun）：Recursive Self-Improvement in AI: A Survey of Claims, Evidence, and Empirical Tests">',
      '<Base title="Is AI Improving Itself? · Qi Sun" description="Qi Sun: Recursive Self-Improvement in AI: A Survey of Claims, Evidence, and Empirical Tests">'),
     (lang_span, ""))
edit("report/site/src/components/EvidenceBubble.astro",
     ("const zh = () => document.documentElement.dataset.lang !== 'en';", "const zh = () => false;"),
     ('placeholder="第三轮为什么变差 / LoRA time limit"', 'placeholder="Why did round 3 get worse? / LoRA time limit"'),
     (lang_span, ""))
edit("report/site/src/layouts/Base.astro",
     ('<html lang="zh-CN" data-lang="zh">', '<html lang="en" data-lang="en">'),
     (re.compile(r"\s*<script is:inline>\s*try \{\s*const saved = localStorage\.getItem\('rsi-lang'\);.*?</script>", re.S), ""),
     ("try { localStorage.setItem('rsi-lang', lang); } catch (e) {}", ""),
     ("apply(root.dataset.lang || 'zh');", "apply('en');"))
# ---- 3. Jekyll skips folders starting with "_", so emit Astro's bundle under assets/ instead of _astro/ ----
edit("report/site/astro.config.mjs", ("  output: 'static',", "  output: 'static',\n  build: { assets: 'assets' },"))
print("patch_public: ok")

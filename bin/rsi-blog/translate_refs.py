"""English edition: translate the reference-list metadata that the report keeps in Chinese.

Runs on report/site/src/data/content.json after build_content.py. Body text is already English; only the
reference titles (`en`) and type notes (`note`) need this. Exits non-zero if any Chinese is left, so a new
reference added to the report shows up here instead of shipping untranslated.
"""
import json
import re
import sys

PATH = sys.argv[1]
CJK = re.compile(r"[　-〿一-鿿＀-￯]")

TITLES = {
    "T-05": 'Schmidhuber (2003/2006), "Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements", arXiv cs/0309048 v5; related versions appeared in LNCS 3394 (2005), ICANN 2005 and *Artificial General Intelligence* (Springer 2006)',
    "T-23": "ICLR 2026 Workshop on AI with Recursive Self-Improvement (Rio de Janeiro, 2026-04-26; organizers include Zhuge, Zeng, Schmidhuber and others)",
    "X-24": 'Weco AI blog, URL path first-evidence-of-recursive-self-improvement (page title not checked verbatim). The Level 2 wording quoted in the text, "ignition, when the system improves its own ability to improve itself", is taken from the note at `research/platform_design.md` line 69',
    "RF-Q9": "Check note 9: not disclosed: which LLM, agent roles, whether it rewrites its own scaffold, number of iterations, compute / GPU-hours / cost.",
    "NV-Q2": "Check note 2: different evaluation harnesses: NV-23–25 were run by Naive on its own in-house AutoResearch harness, while the Recursive numbers come from its article and leaderboard; not a same-harness comparison.",
    "NV-Q6": 'Check note 6: "AI models" are not named: the architecture and NaiveRT parts only say "AI models"; only AutoWM is explicitly run by Naive-N0.5-Flash.',
    "FL-Q7": 'Check note 7: the Eureka Machine contribution is not quantified: "helped develop nearly every part", with no per-component breakdown; "Our bet is…" is explicitly a bet, not a demonstrated result.',
    "AX-Q10": 'Check note 10: which model drives Apex Research, how many iterations, the acceptance criterion, the degree of human involvement and the compute are all unstated. In the Sokoban example, "we identified 36…" indicates manual post-hoc labelling.',
    "AX-43": 'Runs: pass@1 (one run per task) (original: "Every task is run once (pass@1).")',
    "RF-02": 'NanoChat budget: 5 minutes / single GPU (original: "within a fixed five-minute budget on a single GPU")',
    "RF-05": 'Previous SOTA BPB (community best 10-seed mean after removing minor reward hacks): 0.9372 (original: "its mean performance is 0.9372 BPB")',
    "RF-06": 'Recursive NanoChat BPB: 0.9109 (original: "Our system found a solution that reached 0.9109 BPB")',
    "RF-08": 'Reduction in training time to reach the same loss: 1.3x (original: "roughly 1.3x less training time than the best autoresearch@home solution")',
    "RF-11": 'Speedrun target validation loss: 3.28 (original: "Training time required to reach a 3.28 validation loss")',
    "RF-17": 'Recursive speedrun result: 79.7 → 77.5 s (original: "reduced training time from 79.7 seconds to 77.5 seconds")',
    "RF-23": 'SOL-ExecBench kernel tasks: 235 (original: "The benchmark contains 235 kernel-writing tasks derived from real workloads.")',
    "RF-25": 'Previous SOL leaderboard best: 0.699 (original: "from the previous leaderboard best of 0.699")',
    "RF-26": 'Recursive mean SOL score: 0.754 (original: "achieved a mean NVIDIA SOL-ExecBench score of 0.754")',
    "FL-01": 'Total parameters: 40B (original: "Flint has 40 billion total parameters and activates just 2.5 billion per token.")',
    "FL-02": "Active parameters per token: 2.5B (original: same as above)",
    "FL-03": 'Time to build from scratch: under 4 months (original: "built it from scratch in under four months")',
    "FL-07": 'Decode speed on an M4 Pro MacBook Pro: >125 tok/s (original: "more than 125 tokens per second on an M4 Pro MacBook Pro")',
    "NV-43": 'Full speculative round, NaiveRT vs SGLang: 3.4 ms vs 12.3 ms (original: "from 12.3 ms under SGLang to 3.4 ms, a 72.4% reduction")',
    "NV-45": 'Build time: six days (original: "built in six days by human researchers working with AI models")',
    "NV-46": 'Documented optimization trials: 151 (original: "across 151 documented optimization trials")',
    "NV-60": 'Adopted / failed or rolled back / exploratory: 63 / 71 / 17 (original: "63 produced changes that were adopted." "71 failed validation or were rolled back.")',
    "NV-69": 'Cumulative research time: 400 hours (original: "After 400 hours of cumulative research and 15 major experimental rounds")',
    "NV-71": 'AutoWM score on WorldArena-1 Track 1 (EWMScore): 77.43 (original: "reached a score of 77.43 under the public WorldArena-1 Track 1 evaluation protocol")',
    "AX-01": 'Total parameters: 35B (original: "This 35B general-purpose model is based on Qwen3.6-35B-A3B")',
    "AX-02": 'Parameter split: 35B total / ~3B active (original: "35B total parameters with approximately 3B activated per token")',
    "AX-22": 'Explore / retrain budget (shared by Sokoban and DDPO): 4 h / 12 h (original: "4 hours to explore training strategies and 12 hours to retrain the model")',
    "AX-23": 'Sokoban unseen evaluation levels: 512 (original: "performance evaluated on 512 unseen puzzle levels")',
    "AX-25": 'Sokoban success rate, Apex-trained model vs base: 24.4% / 11.7% (original: "24.4% success rate on 512 unseen levels, more than doubling the base model\'s 11.7%")',
}
NOTES = {
    "Preprint（另有 PR 版本）": "Preprint (a peer-reviewed version also exists)",
    "Preprint。有二手来源称它在 AGI-15 以 PR 形式发表，本次未核实": "Preprint. A secondary source says it was published peer-reviewed at AGI-15; not verified here",
    "PR（书章）。原文是扫描版，无法抽取文字；下面的段落按 Chalmers 2010 和 Yudkowsky 2013 的逐字转引核对": "Peer-reviewed (book chapter). The original is a scan with no extractable text; passages were checked against verbatim quotations in Chalmers 2010 and Yudkowsky 2013",
    "工作坊（会议存在已核实；是否 archival 页面上没写）": "Workshop (existence verified; whether archival is not stated on the page)",
    "PR（期刊）": "Peer-reviewed (journal)",
    "Preprint（个人草稿，未发表）": "Preprint (personal draft, unpublished)",
    "公司博客": "Company blog",
    'Essay/Blog（研究机构），基于 Erdil, Besiroglu & Ho, "Estimating Idea Production: A Methodological Survey", arXiv 2405.10494':
        'Essay/Blog (research organization), based on Erdil, Besiroglu & Ho, "Estimating Idea Production: A Methodological Survey", arXiv 2405.10494',
    "Preprint/Essay（研究机构）": "Preprint/Essay (research organization)",
    "外部评估报告": "External evaluation report",
    "arXiv（会议见第 5 节）": "arXiv (venue: see Section 5)",
    "arXiv 预印本": "arXiv preprint",
    "peer-reviewed（PDF 注明 COLM 2024）": "peer-reviewed (PDF states COLM 2024)",
    "peer-reviewed（PDF 页眉注明 ICLR 2026）": "peer-reviewed (PDF header states ICLR 2026)",
    "见原文件": "See source file",
}
LEDGER = [  # generic pieces of "证据台账 RF-02 · 自报" style notes
    ("证据台账", "Evidence ledger"), ("不一致 / 待核", "inconsistent / to verify"), ("自报", "self-reported"),
    ("（benchmark 属性，源自 NVIDIA）", " (benchmark property, from NVIDIA)"), ("（推算核对：", " (arithmetic check: "), ("；", "; "), ("）", ")"),
]

PUNCT = [("（", " ("), ("）", ")"), ("：", ": "), ("，", ", "), ("；", "; "), ("、", ", ")]


def punct(t):
    for a, b in PUNCT:
        t = t.replace(a, b)
    return re.sub(r"  +", " ", t).replace("( ", "(")


c = json.load(open(PATH))
left = []
for r in c["refs"]:
    if r["key"] in TITLES:
        r["en"] = TITLES[r["key"]]
    note = r.get("note") or ""
    if note in NOTES:
        r["note"] = NOTES[note]
    elif note.startswith("证据台账"):
        for a, b in LEDGER:
            note = note.replace(a, b)
        r["note"] = note
    for k in ("en", "note", "loc"):
        if r.get(k):
            r[k] = punct(r[k])
    for k in ("en", "note", "loc", "work"):
        if CJK.search(r.get(k) or ""):
            left.append(f"  ref {r['n']} [{r['key']}] {k}: {r[k]}")
    for j in r.get("jumps", []):
        if CJK.search(j.get("label", "")):
            left.append(f"  ref {r['n']} [{r['key']}] jump: {j['label']}")
if left:
    sys.exit("translate_refs: untranslated reference text (add it to bin/rsi-blog/translate_refs.py):\n" + "\n".join(left))
json.dump(c, open(PATH, "w"), ensure_ascii=False, indent=1)
print(f"translate_refs: {len(c['refs'])} refs in English")

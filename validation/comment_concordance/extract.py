import json, os, re
BASE="D:/code/psychohistory_v04_bundle"
DATA=BASE+"/validation/comment_concordance/data"

JUNK_AUTHORS={"AutoModerator","[deleted]"}
def removed(c):
    b=(c.get("body") or "").strip()
    if b in ("[removed]","[deleted]",""): return True
    if c.get("author") in JUNK_AUTHORS: return True
    return False

def is_mod_note(b):
    bl=b.lower()
    return ("this thread" in bl and ("removed" in bl or "rule" in bl)) or bl.startswith("please note") or "top-level comment" in bl or "i have removed" in bl[:120]

def load(pid):
    j=json.load(open(f"{DATA}/{pid}.json",encoding="utf-8"))
    return j.get("data",[])

EXPERT_FLAIRS={"Quality Contributor","AE Team","REN Team"}
def is_expert(c):
    return (c.get("author_flair_text") or "").strip() in EXPERT_FLAIRS

def best_answer(data):
    """AskEconomics vetted answer = substantive comment by a flaired Quality Contributor /
    AE Team / REN Team member, preferring top-level. Reddit score is only a weak tiebreak,
    because popular non-expert takes routinely outscore (or outlive) the approved answer.
    Falls back to the best surviving substantive comment if no flaired answer is present."""
    surv=[c for c in data if not removed(c) and not is_mod_note(c.get("body") or "")]
    if not surv: return None,"no-survivors"
    def substantive(pool):
        s=[c for c in pool if len(c.get("body") or "")>=120]
        return s or pool
    def toplevel(pool): return [c for c in pool if str(c.get("parent_id","")).startswith("t3_")]
    def rank(c): return (len(c.get("body") or "")/400.0) + (c.get("score") or 0)*0.25

    experts=substantive([c for c in surv if is_expert(c)])
    if experts:
        tl=toplevel(experts)
        pool=tl if tl else experts
        best=max(pool,key=rank)
        return best, ("expert-top-level" if best in tl else "expert-nested")
    sub=substantive(surv)
    tl=toplevel(sub)
    pool=tl if tl else sub
    best=max(pool,key=rank)
    return best, ("nonexpert-top-level" if best in tl else "nonexpert-nested")

if __name__=="__main__":
    posts=[json.loads(l) for l in open(BASE+"/.claude/skills/psychohistory/corpus/posts.jsonl",encoding="utf-8")]
    usable=0; nores=0
    for p in posts:
        data=load(p["id"])
        ans,src=best_answer(data)
        if ans and len(ans.get("body") or "")>=120:
            usable+=1
        else:
            nores+=1
    print("usable answers:",usable,"no-usable:",nores)

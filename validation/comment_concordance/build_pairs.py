import json
from extract import load, best_answer
import os
os.chdir("D:/code/psychohistory_v04_bundle/validation/comment_concordance")
BASE="D:/code/psychohistory_v04_bundle"
posts={json.loads(l)["id"]:json.loads(l) for l in open(BASE+"/.claude/skills/psychohistory/corpus/posts.jsonl",encoding="utf-8")}
models={}
for l in open(BASE+"/validation/lethain_models.jsonl",encoding="utf-8"):
    d=json.loads(l); models[d["id"]]=d

pairs=[]
for pid,m in models.items():
    if not (m.get("model_dsl") or m.get("model_template")):
        continue
    data=load(pid)
    ans,src=best_answer(data)
    body=(ans.get("body") if ans else "") or ""
    pairs.append({
        "id":pid,
        "title":posts[pid]["title"],
        "model_template":m.get("model_template"),
        "model_conclusion":(m.get("qualitative_result","")+" || "+m.get("justification","")),
        "old_validation":m.get("validation"),
        "answer_author":ans.get("author") if ans else None,
        "answer_score":ans.get("score") if ans else None,
        "answer_src":src,
        "answer_len":len(body),
        "answer_body":body[:3500],
    })
json.dump(pairs,open("_pairs.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("pairs (posts with model):",len(pairs))
print("answers with len>=120:",sum(1 for p in pairs if p["answer_len"]>=120))

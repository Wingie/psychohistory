import json, os, time, urllib.request, urllib.error

BASE = "D:/code/psychohistory_v04_bundle"
OUT  = BASE + "/validation/comment_concordance"
DATA = OUT + "/data"
os.makedirs(DATA, exist_ok=True)
API = "https://arctic-shift.photon-reddit.com/api/comments/search"

def fetch(link_id, after=None, retries=4):
    url = f"{API}?link_id={link_id}&limit=100&sort=desc"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"psychohistory-concordance/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503):
                time.sleep(5*(attempt+1)); continue
            return {"_error": f"HTTP {e.code}"}
        except Exception as e:
            time.sleep(4*(attempt+1))
            if attempt==retries-1: return {"_error": str(e)}
    return {"_error":"retries-exhausted"}

posts=[json.loads(l) for l in open(BASE+"/.claude/skills/psychohistory/corpus/posts.jsonl",encoding="utf-8")]
print("posts:",len(posts))
log=[]
for i,p in enumerate(posts):
    pid=p["id"]
    fn=f"{DATA}/{pid}.json"
    if os.path.exists(fn):
        try:
            j=json.load(open(fn,encoding="utf-8"))
            log.append((pid,len(j.get("data",[])),"cached")); 
            continue
        except: pass
    res=fetch(pid)
    if "_error" in res:
        json.dump(res,open(fn,"w",encoding="utf-8"))
        log.append((pid,0,res["_error"]))
    else:
        data=res.get("data",[])
        json.dump({"data":data},open(fn,"w",encoding="utf-8"))
        log.append((pid,len(data),"ok"))
    print(f"{i+1}/{len(posts)} {pid} -> {log[-1][1:]}")
    time.sleep(1.2)

ok=sum(1 for _,n,s in log if s in ("ok","cached") and n>0)
err=sum(1 for _,n,s in log if s not in ("ok","cached"))
print("DONE ok-with-data:",ok,"errors:",err,"empty:",sum(1 for _,n,s in log if s in('ok','cached') and n==0))
json.dump(log,open(OUT+"/_harvest_log.json","w"))

import re, os
from collections import Counter

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
txt = open("psychohistory.tex", encoding="utf-8").read()

print("=== em dashes (---) ===", txt.count("---"))

begins = Counter(re.findall(r"\\begin\{(\w+\*?)\}", txt))
ends = Counter(re.findall(r"\\end\{(\w+\*?)\}", txt))
bad = False
for env in sorted(set(begins) | set(ends)):
    if begins[env] != ends[env]:
        print("UNBALANCED", env, begins[env], ends[env])
        bad = True
print("total begin", sum(begins.values()), "total end", sum(ends.values()))
print("ALL ENVS BALANCED" if not bad else "BALANCE ERROR")

print("--- includegraphics paths ---")
paths = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", txt)
allok = True
for p in paths:
    ok = os.path.exists(p)
    if not ok:
        allok = False
    print(("OK  " if ok else "MISSING "), p)
print("ALL FIGURE PATHS EXIST" if allok else "MISSING FILES")

# labels vs refs
labels = set(re.findall(r"\\label\{([^}]+)\}", txt))
refs = set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", txt))
undef_refs = refs - labels
print("--- undefined \\ref/\\eqref ---", undef_refs if undef_refs else "NONE")

# cites vs bibitems
bibs = set(re.findall(r"\\bibitem\{([^}]+)\}", txt))
cites = set()
for grp in re.findall(r"\\cite\{([^}]+)\}", txt):
    for c in grp.split(","):
        cites.add(c.strip())
undef_cites = cites - bibs
print("--- undefined \\cite ---", undef_cites if undef_cites else "NONE")

# unreferenced labels (informational, not an error)
unref = labels - refs
print("--- labels never \\ref'd (informational) ---", unref if unref else "NONE")

# Pre-registration seal (FA-0)

This file is the immutable record that the two pre-registration documents digested below
were committed BEFORE the results they judge. It discharges FA-0 (the external-timestamp
step) for those two files only, to the extent a public git history allows, and states
honestly what it does and does not prove. It does **not** cover the later neff_v2, neff_v3,
neff_v4 or bifurcation_mix pre-registrations; see the scope caveat below, which names each
one and says what stands behind it instead.

## What is sealed

SHA-256 digests of the frozen pre-registration documents, as of this commit:

| file | sha256 |
|---|---|
| `validation/PRE_REGISTRATION.md` (the 8 falsifiers, thresholds X,Y,Z,rho0,M,piB,AUC,m,delta; plus ii' the dynamic N_eff collapse, f=0.30) | `c3b437acf7aebaca2677c64279dbfcf32f2aa224567fdaefeeb3740142b96513` |
| `validation/wikipedia/PRE_REGISTRATION_wiki.md` (the ii' Wikipedia run thresholds, frozen before harvest) | `e01042f4a8689a5ab53d9ae178cc4f920186fda30f1c970ba65b89d35c169cf9` |

Recompute with `sha256sum <file>` and compare. Any later edit to those files changes the
digest, so this commit pins their exact pre-result content.

## The timestamp mechanism, and its honest limits

- **Local git commit.** The commit that introduces this file places the digests in an
  append-only history. A local commit alone is not a third-party timestamp (the author
  controls the clock).
- **Public push (the actual third-party anchor).** When this commit is pushed to the
  GitHub remote (`origin`, github.com/Wingie/comfyui-experiments), GitHub records the
  receive time independently of the author. That GitHub-side commit timestamp is the
  external lodge: it proves the digests existed no later than the push.
- **Not yet done (stronger anchors, named for honesty).** OpenTimestamps (a Bitcoin-anchored
  `.ots` proof) is not installed here; an OSF registration DOI is not lodged. Either would
  be a stronger, platform-independent anchor than a GitHub timestamp, and remains the
  recommended upgrade if this program goes to a venue that demands it.

## Scope caveat (exactly which tests this seal covers, and which it does not)

**Covered: the two files digested above, and nothing else.** The digests pin the falsifiers
as specified in `validation/PRE_REGISTRATION.md` and `validation/wikipedia/PRE_REGISTRATION_wiki.md`.
No other pre-registration in this tree is pinned by a digest here.

**Not covered.** Every later pre-registration, named individually so that nobody has to
infer the gap from an absence:

| pre-registration | digest in this file | what actually stands behind it |
|---|---|---|
| `validation/neff_v2/PRE_REGISTRATION_neff_v2.md` (re-derived f, clean-null rule) | none | authored before its own analysis, same working session, same author |
| `validation/bifurcation_mix/PREREG.md` (the B/N/R rule for iii') | none | same |
| `validation/neff_v3/PRE_REGISTRATION_neff_v3.md` (f=0.3936, the four-condition rule) | none | same |
| `validation/neff_v4/PRE_REGISTRATION_neff_v4.md` (the specificity-primary binomial rule) | none | same |

The neff_v3 and neff_v4 entries were missing from this file entirely until this revision: a
reader grepping for `neff_v3` or `neff_v4` here got nothing, while the word SEALED travelled
with those two runs through six other documents and the paper's conclusion. That was the
defect, and it was ours. `validation/neff_v4/RESULTS.md` states that its threshold was
committed "to be folded into the FA-0 hash seal"; it was never folded in, and this table is
the record of that.

**The git history carries no ordering for v3 or v4 either.** `git log --follow` on
`PRE_REGISTRATION_neff_v4.md`, `roster_v4.py`, `harvest_v4.py`, `analyze_v4.py`,
`result_neff_v4.json` and `neff_v4/RESULTS.md` shows all six entering the history in a single
commit, `aaff92349990b85a9bb3300638ca450cedf8d1fd` (2026-06-17): the same commit for the
threshold and for the result it judges. The same holds for the neff_v3 artefacts
(`PRE_REGISTRATION_neff_v3.md`, `derive_f_v3.py`, `derive_f_v3.json`, `analyze_v3.py`,
`RESULTS.md`). Later commits to those files are corrections written after the fact, this one
among them, and they do not supply the missing ordering. So for those two runs
the history supplies zero temporal separation between threshold and result: the ordering
rests on the in-file statement that the thresholds were fixed first, and on nothing else.

**So what does the word SEALED mean when it is applied to neff_v3 and neff_v4 elsewhere in
this repository?** It means: the threshold is written down in a file that its author states
was written before the analysis was run, within a single working session, and committed
together with the results. It does **not** mean a digest in this file, a third-party
timestamp, or a commit ordering that an outside reader can check. Any ledger entry, README
line or paper sentence that carries the bare word SEALED for v3 or v4 is overclaiming by
exactly that much, and should be read as "in-session pre-registered, not independently
timestamped".

**Why we are not simply adding v3 and v4 digests now.** A digest computed after the results
are known certifies nothing; back-filling this table would convert an honest gap into a
false assurance. The repair is prospective and cheap: for the next run, commit and push the
pre-registration in one commit, and the results in a strictly later one, so the public
receive-times carry the ordering; then digest it here.

## What the seal does NOT establish

It does not make any test PASS, and it does not make the program correct. It only removes the
authors' freedom to move the goalposts after seeing the data, for the thresholds it pins.
A confirmed program raises the governance stakes; a sealed threshold only keeps the scoring
honest.

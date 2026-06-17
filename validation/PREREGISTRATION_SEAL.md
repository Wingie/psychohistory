# Pre-registration seal (FA-0)

This file is the immutable record that the psychohistory falsification thresholds were
committed BEFORE the results they judge. It discharges FA-0 (the external-timestamp step)
to the extent a public git history allows, and states honestly what it does and does not
prove.

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

## Scope caveat (which tests this seal covers)

This seal covers the falsifiers as specified in the two files above. Two later
pre-registrations written this session, `validation/neff_v2/PRE_REGISTRATION_neff_v2.md`
(the re-derived f and clean-null rule for the sealed-pass attempt) and
`validation/bifurcation_mix/PREREG.md` (the B/N/R rule for iii'), were each authored before
their own analysis was run, but in a single working session rather than under an independent
prior timestamp; they are sealed by descendant commits, and their integrity rests on the
in-file statement that thresholds were fixed before results plus this history, not on an
independent third-party clock between threshold and result. We state that plainly rather
than overclaim a separation the workflow did not have.

## What the seal does NOT establish

It does not make any test PASS, and it does not make the program correct. It only removes the
authors' freedom to move the goalposts after seeing the data, for the thresholds it pins.
A confirmed program raises the governance stakes; a sealed threshold only keeps the scoring
honest.

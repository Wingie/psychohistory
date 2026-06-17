# Responsible-use and dual-use notice

This document states the responsible-use policy for the *Conditions for Predictable Social Dynamics* framework. It is consistent with the governance section of the paper (`psychohistory.tex`, §Governance) and with the enforced SAFETY guardrail in the Claude skill (`.claude/skills/psychohistory/SKILL.md`). If you build on this work, you are asked to honor the same split.

## The framework is dual-use

The framework describes a **prediction–control duality**. At a critical transition the correlation length diverges, the effective number of independent blocks collapses toward one, and the same divergence of susceptibility that *destroys predictability* simultaneously *maximizes controllability*. Concretely: **the moment that gives the cleanest early warning of a transition is also the moment of maximum manipulability of the population.** The machinery that detects a brewing bank run, cascade, or panic is, read adversarially, the theory of operation of low-cost population steering. The capability and its mitigations therefore travel together, and this notice is part of the work, not an afterthought to it.

## What is provided, and what is deliberately withheld

**Provided openly (defensive / early-warning):**

- the forward model, observation operators, and ensemble-assimilation loop (the engine as a *monitor*);
- the regime monitor and skill-horizon estimate;
- the structural and concentration observables (block detection, N_eff, HHI/Gini, semantic critical-slowing-down);
- the **mechanism-classifier** form of the operator detector (gradual-internal-buildup vs sudden-external-shock; *aggregate* concentration statistics);
- the validation code, the aggregate results, and the pre-registration protocol.

**Deliberately NOT provided (offensive / control-synthesis):**

- the **optimal-intervention solver** — any objective-driven controller that selects *which* intervention to apply;
- the **message-selection / susceptible-block targeting objective** — any "which message switches this cascade" recipe or rule for choosing *which* fixed point to drive a population toward;
- any **per-individual targeting / neutralization** artifact, exploit-timing schedule, or per-individual buildup score tuned to identify a specific person pre-onset.

The belief-closure simulator (the fixed-point iteration over block-conditioned agents) is the one offensive-dominant component. Its *interface* may be named ("iterate to a fixed point"); an *objective that selects a fixed point* is withheld.

## The operator-detector is for accountability, not targeting

Detecting a major-player / operator signal is itself dual-use. It is defensible **only** at the **mechanism-classifier grain** — a population-facing warning that an operator is active, expressed as a classification (internal buildup vs external shock) and as aggregate concentration statistics. It must **never** be turned into a targeting tool against a named individual: not a per-individual identifier, not a pre-onset alarm against a person, not a warrant. The individual — not the block — is the unit of moral concern. **A buildup flag is a warning to a population, never a warrant against a person.** The raw harvested rosters and per-block signal traces are themselves controller-precursor data and are released only at the aggregate, mechanism-classifier level for this reason.

## Conditions under which any control use could be legitimate

The paper does not claim control use is *never* legitimate (a central bank's lender-of-last-resort guarantee is a legitimate intervention at criticality). It names the **binding minimum conditions**, and declares that any deployment lacking them is illegitimate by the work's own standard:

1. **Externally-authored, externally-revisable objective.** The controller's objective function must be authored outside the controller and remain revisable *during* operation, by an author constituted before deployment, independent of the controller, and accountable to the population acted upon. An objective laundered through pretrained model weights satisfies this only nominally and must be treated as part of the auditable objective.
2. **Auditable, contemporaneously-disclosed intervention log.** The *existence* of every critical-regime intervention (not necessarily its sealed contents) must be disclosed contemporaneously, to a record the controlled population can audit, with the content-disclosure lag bounded to the reversibility timescale.
3. **Separation of monitor from controller.** No single agent may hold both the regime monitor and the control input. The seer must be separated from the hand, run as separately operated systems with separate authority.
4. **The chooser sits outside the machine.** No system can certify the rightness of the world it is about to impose; the decisive objective choice must rest with an external human authority, not with the Plan.

The invariant danger is the **concentration** of the monitor and the control input in one locus accountable to no one — private, public, or public-private fusion alike. Scientific validation of the program, if it ever comes, *raises* these governance stakes rather than discharging them.

## Ask of anyone building on this

Keep the split. Build the **monitor, not the manipulator**. Publish defensive components openly; withhold the control-synthesis layer; hold any population-scale attention corpus under the same monitor-versus-hand separation and auditable-construction conditions the paper requires of the reanalysis corpus. If your use crosses into steering, manipulating, triggering, suppressing, or targeting a population or an individual, it is the withheld use, and this work asks you not to do it.

# Axiom One: The Steering Envelope

*The first intervention axiom of the psychohistory program. Postulated 2026.
The instrument is [here](../site/steering_sim.html); the code, data and
wager terms live in
[`steering_envelope/`](https://github.com/wingie/psychohistory/tree/main/steering_envelope).*

---

Seldon's fictional science had two premises: enough people, and laws that
hold whether or not any one of them believes. The real, bounded version we
are building in this repository has spent its first years on the passive
side of that idea: conservation of attention, community blocks,
criticality, the collapse of effective independence before a cascade. All
of it watches.

This module is the first axiom about acting. Here it is.

**A society survives a technology in proportion to the control it can
exert over that technology's speed. Uncontrolled acceleration crashes.
Forced deceleration also crashes, later and harder. What survives is
constant controlled speed: brake into the corners, accelerate out of
them, never exceed the grip.**

I am stating that with conviction, not with a shrug. Most theories worth
having were postulated long before they were proved, and the way you earn
the proof is by writing the claim down plainly, building the instrument,
and letting every new episode of history score it. That is what this
module does. Time will tell. We wrote it down first.

## Start with fire

Strip away everything modern and the axiom is already there at the first
campfire.

A tribe discovers fire. What are its choices? It can keep the secret,
post guards around the hearth, and enjoy an advantage until the night a
rival steals an ember or the keeper of the flame dies with the trick. It
can sell the secret, trade fire for food, for alliance, for marriage,
which means the secret moves, but slowly, along the channels of who can
pay. Or it can teach the secret, and then fire is simply something humans
have, and no tribe can hold another hostage with it, and every hearth in
the valley now needs the same thing: rules. Keep it off the dry grass.
Bank it at night. Watch the children.

Notice what just happened. The three choices are the three acceleration
mechanisms the modern discourse thinks it invented. Hoard the capability.
Gate and sell the capability. Share the capability. And notice the fourth
thing, the one that appears in every branch: the rules of the hearth. The
firebreak. The watcher. That is steering capacity, and it is the only
part of the story that decides whether the valley burns.

So when I write v, speed, I do not just mean how fast the frontier moves.
I mean how capability moves through the network of tribes: hoarded,
sold, or shared. And when I write s, steering, I mean the accumulated
stock of hearth rules: verification, licensure, inspectorates, incident
channels, institutions that can absorb a shock. The axiom says survival
is decided by the ratio of the two.

## The six states

History keeps ending transitions in the same small set of ways. The model
names six, and each one has a face.

**ARRIVED.** You cross the transition first, intact, and you set its
terms. Britain crossed the railway transition first and wrote the gauge,
the law, and the timetable of the industrial world.

**CONVOY.** The transition arrives as a pack, because the knowledge was
shared or standardized until nobody held a decisive edge. Once everyone
knows the secret of fire, nobody has an advantage, and everybody has
fire. Rail gauge standardization did this. Open protocols did this to
networking. Free and open source software does this on purpose: it is
the deliberate breaking of the hoard, knowledge moved directly to all.
Convoy is not a consolation prize. It is the highest-yield state history
offers, because the gains arrive without the wreck.

**SHOTGUN.** Someone else crosses first and you live in the world they
chose. Tokugawa Japan held itself out of the industrial transition for
two centuries, and then Perry's black ships arrived and the terms were
not Japan's. The stopper does not get a parked world. He gets a world
decided from the passenger seat.

**HELD.** Nobody crosses. The transition is refused or indefinitely
deferred. Rare, temporary, and paid for in everything the transition
would have bought.

**CRASHED.** You take a corner beyond your control authority and lose
the machine. Chernobyl is the clean case: a reactor design pushed by a
program that outran its own safety culture, a test run at night against
the manual, and a state that lost not just a reactor but a large part of
its remaining legitimacy.

**PILEUP.** The coupled crash. Everyone goes down together because
everyone was leaning on everyone. This is the one the axiom cares most
about, and its archetype is old. The Late Bronze Age was a dozen palace
economies locked in one trade network, tin from one direction, copper
from another, grain moving between kings who wrote each other letters.
Every palace hoarded its own advantages, and none could stand alone.
Around 1200 BC the network took a hit, and within a lifetime nearly
every palace from Pylos to Ugarit was ash. Writing itself was lost in
Greece for four centuries. That is what a pileup is: not a crash of one
driver but the failure of a formation. We rebuilt the same shape in 2008
with balance sheets instead of bronze.

Which of the six states you get is not destiny and it is not luck. That
is the axiom's whole content: the state is selected by the ratio of
speed to steering at the corners.

## One law

Now the equation, and it is deliberately small. When a transition hits a
corner, a critical threshold where control is actually contested, the
probability you lose the machine is logistic in speed times corner
tightness over steering capacity:

    h = sigma( beta * ( v*k / (s*c0) - 1 ) )

Inside the envelope, v times k below s, hazard is low. Outside it,
hazard saturates. The edge is ratio one. Corner tightness k is how
unforgiving this particular transition is: a tighter corner for nuclear
material than for spreadsheets, tighter for autonomous weapons than for
chess engines.

Too simple? So is F equals ma. Simple is what lets the data vote.

## The mechanisms history invented

Once you see steering as a real quantity, you start recognizing the
machinery every era built to supply it. Each mechanism is a different
setting of the dials, and history has run them all.

Secrecy, the NDA, the guarded hearth. This buys a private v advantage
and makes the whole formation brittle, because hoarded knowledge dies
with its keepers and hoarding civilizations cannot call for help. The
Bronze Age palaces ran this setting into the pileup.

The patent. A genuinely clever compromise: sell the secret of fire, but
the price is publication and the monopoly expires. It is a timed gate,
a throttled convoy. Societies that adopted it got compounding disclosure
instead of hereditary guild secrets.

The conscience endowment. Nobel made his fortune on explosives and
endowed the prize with it. That is steering bought retroactively, guilt
converted into an institution that redirects ambition toward shared
knowledge.

The apprenticeship and the license. Some knowledge is gated not by price
but by time and demonstrated competence: medicine, flight, and, when we
still bothered, finance. Gating by experience is a steering mechanism
disguised as a career path.

The treaty with an inspectorate. The nuclear case. After 1945 the powers
looked at the tightest corner ever discovered and did something without
precedent: they built an agency whose whole purpose is to keep wayward
drivers from taking that corner alone. Safeguards, inspections,
enrichment thresholds. It is the purest institutional form of the
coordination dial, and civil nuclear power's event record since the
regime matured is the receipt.

The commons. FOSS, open protocols, open science. Maximum sharing, which
reads as maximum recklessness until you notice what it does to the
distribution of drivers: nobody holds a decisive edge, so nobody is
forced into a desperate corner, and every eye is on the same code. The
commons is a coordination mechanism wearing an anarchist jacket.

And the null mechanism, the control group that runs itself for us right
now: crypto. No license, no inspectorate, no expiry, coordination near
zero by design. The result is the purest uncoordinated field in modern
economic history, and it looks exactly like the model says an
uncoordinated field looks: perpetual small crashes, NFT manias, rug
pulls, exchange pileups, extraordinary innovation and no floor under
anyone.

## Steering is not suppression

Here is the misreading I most want to kill, because it is the one
governments commit.

Steering does not mean preventing every crash. A hand that only ever
brakes is not steering, it is storing the crash. Suppress every small
correction, guarantee every bank, refuse every recession, and you do not
delete the energy, you bank it in the fuel tank for a bigger corner.
Finance shows both failure modes side by side. Repeal Glass-Steagall,
remove grip while credit accelerates, and you get 2008. But equally,
administrations that lean on the central bank to abolish every downturn
are not steering either. They are welding the brake pedal to the floor
of the future, moving the crash later and amplifying it. The Minsky
reading and the forest-fire reading are the same reading: small fires
clear the underbrush.

The axiom is symmetric and I mean it symmetrically. Uncontrolled
acceleration crashes now. Enforced deceleration and suppression crash
later, bigger. The surviving policy is the racing line: constant
sustainable speed, deceleration into the corners, acceleration out of
them. In the instrument this is exactly why the HELD state loses and why
the s/acc preset brakes early and then runs fast on accumulated grip.

## Rehypothesizing the past

A theory of steering should be able to walk back through history and
label the episodes. Here is the opening of that catalog. Each entry is
an episode, the mechanism in force, and the state it selected.

The Late Bronze Age: hoarding under tight coupling, PILEUP. The golden
age of piracy: the sea lanes were a commons with no steering at all,
and when the losses grew intolerable the states bought grip in the form
of navies and admiralty law, closing an ungoverned corner; the corner
itself never went away, which is why a single strait off Iran can still
put the world economy on notice. Railway standardization: forced
knowledge sharing, CONVOY. Nuclear plus the IAEA: the tightest corner,
taken slowly, in formation, and the only major technology whose
worst-case tail has so far been held by treaty. Nobel and the patent
system: conversion mechanisms, private speed turned into public grip.
The socialist experiments: enforced deceleration of the market
transition, and every one of them either crashed, opened, or converged
back toward market speed under party grip; look at China's hybrid
housing market for what re-steering mid-corner looks like. Crypto: the
running control group, coordination pinned to zero. GameStop, January
2021: a contested steering event, hedge funds trying to steer a company
into bankruptcy, a crowd counter-steering, and the whole thing legible
in advance to anyone reading the ratio, which one retail analyst
famously did. The world is steered, constantly, by people who believe
they can shape which future arrives. The only question the axiom asks
is whether the steering is matched to the speed.

One more entry belongs on this list as a standing invitation: speed
limits themselves. There exist motorways with and without them, in
otherwise similar countries, with published crash data. That is a
natural experiment aimed directly at the axiom, and it is queued as the
next domain study.

## The record so far

Rehypothesis is cheap; fits are not. So we ran the axiom against five
domains of public data, windows and losing conditions frozen in the
README before the run. The full tables are in the repository. The short
version:

On the roads, the literal case, America multiplied its driven miles a
hundredfold while deaths per mile fell twenty-fold, and in the strict
first-difference test both speed and steering carry independent signal.
In aviation, honesty compels the concession: the oversight stack
explains the safety collapse so completely that speed adds nothing
measurable; aviation reads as a domain the stoppers can cite, and we
log it against ourselves. In finance, the flagship, 18 countries and
145 years of the Jorda-Schularick-Taylor panel: the famous credit-boom
result reproduces, the steering term improves it at odds of billions to
one, and the single best out-of-sample predictor of systemic crisis,
holding out whole decades, is the ratio v/s. The quiet period of 1945
to 1972, fast growth under heavy grip and nearly zero crises, sits in
that data like a signed confession. Nuclear, too small to fit, is
consistent: thirteen times the event rate in fast-build young-regulator
decades. And for AI there is no outcome data yet, so we publish the
leading indicator instead: AI's ratio spiked above every historical
corner band around 2015, and on crude public proxies has come down
since as policy and evals grew, with the loud caveat that a policy
count is not grip any more than a printed rulebook is a driver.

Three of four finished domains hold the axiom. One dissents. The
flagship holds it out-of-sample, which is the test that matters. That
is what a young law is supposed to look like when it is right: scarred,
not spotless.

## The mean field, or why your virtue is not enough

The deepest result in the module is not about any single driver. Replace
the rival with a field of sixteen drivers drawing their throttle from a
distribution, couple crashes to their neighbours, and ask: what buys an
already-careful driver more survival, another unit of private caution or
another unit of field-wide coordination? On every tested point of the
diligent regime, coordination wins, nine grid points out of nine. And in
the household layer, where every outcome is converted into hours of work
per week for food, shelter and energy across eight very different
tribes, the same truth lands harder: with coordination live, the
steering policy wins every tribe's worst decade that it does not tie.
With coordination forced to zero, every single row ties. Your private
virtue keeps your lane. Only coordination reaches anyone's kitchen.

This is the psychohistory of it. The race is a mean-field game, the same
L5 mathematics this repository uses for bank runs. Everyone racing
because everyone expects a race is a self-consistent equilibrium. So is
a held norm. The coordination dial is the order parameter that selects
between them, and treaties, standards bodies, inspectorates and commons
are how civilizations have always moved it.

## The wager

An axiom stated with conviction still names the terms on which it loses.
Ours are frozen in the repository: if the steering term had added
nothing beyond speed across the fittable record, the axiom would be
decoration, and we said so before running. It survived. Going forward
the catalog only grows: every new transition, every natural experiment,
every autobahn table and strait blockade and model release is another
scoring event. Theories are often proved years after they are
postulated. The postulate is now on the record, timestamped, with its
instrument public and its data fetchable by anyone.

So, the call, by seat.

If you build: publish your envelope. Your corner list, your grip
metrics, and the rule that connects them. "We slow when X" is a
falsifiable safety culture. Vibes are not.

If you govern: fund grip, not just brakes, and never confuse
suppression with steering. The quiet period grew fast with its hands on
the wheel. The administrations that abolish every small correction are
buying the big one.

If you argue: stop scoring this debate as gas against brakes. The axis
that predicts the record is grip against speed. Ask every accelerationist
where the steering is. Ask every stopper whose hands they are leaving on
the wheel.

The engine is real. The corners are real. A century of data says the
ratio decides. Drive fast. Never faster than you can steer.

*Wingston Sharon, 2026. Axiom One of the psychohistory program. Code,
frozen wager terms and all datasets:
[`steering_envelope/`](https://github.com/wingie/psychohistory/tree/main/steering_envelope).
This page inherits the repository's [dual-use notice](../ETHICS.md).*

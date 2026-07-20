# The Steering Envelope

*s/acc, rendered as a hazard model and tested on a century of public data.
A module of the psychohistory project. The interactive instrument is
[here](../site/steering_sim.html); the code and validation suite live in
[`steering_envelope/`](https://github.com/wingie/psychohistory/tree/main/steering_envelope).*

---

In the valley right now, "decel" is a slur. Fine. I am not a decel.

I hold one axiom. Never drive a car faster than you can steer it.

That is the whole position. Everything else in this module is me trying to
turn that sentence into an equation, the equation into a simulator, and the
simulator into something a century of public data can embarrass.

## One law

Here is the equation. When a technology transition hits a critical
threshold, call it a corner, the chance you lose control is logistic in the
ratio of your speed to your grip:

    h = sigma( beta * ( v*k / (s*c0) - 1 ) )

Speed v is deployment velocity. Grip s is steering capacity, and I mean
concrete things by that: interpretability, evals, verification regimes,
incident channels, compute you actually own, institutions that can absorb a
shock without shattering. Corner tightness k says how unforgiving this
particular transition is. When v times k is smaller than s, you are inside
the envelope and the hazard is small. When it is bigger, the hazard
saturates toward one. The edge of the envelope is exactly ratio one.

Is that too simple? Of course it is too simple. So is F equals ma. The
question is never whether a law is simple. The question is whether the data
holds it or laughs at it. We will get to the data.

## Four flags, one dashboard

What do you accelerate first? That single question sorts the whole
discourse into a two-by-two.

Accelerate the engine and you get e/acc. Give it its due. Permissionless
innovation has an astonishing welfare record. Electrification, aviation,
the internet. Most catastrophic forecasts about new technology were wrong,
and the costs of friction compound invisibly, in drugs never invented and
growth never compounded. I concede all of it. But thermodynamic teleology
has no term for a corner. It optimizes expected speed when the thing that
matters is speed conditioned on survival. An engine has no opinion about
walls.

Accelerate the armor and you get d/acc, Vitalik Buterin's flag, and it is
the nearest relative of mine. Build defense-dominant technology. Favor the
shield over the sword. It composes beautifully with what I am saying. But
notice what d/acc lacks: a speed governor. It asks which car to build and
never how fast any car may be driven. And offense versus defense is often
unknowable before the fact. The same biology tools cut both ways.

Accelerate the driver and you get w/acc, which as far as I can tell is an
unclaimed letter, so let me claim a reading for it: wisdom acceleration.
Grow the judgment, the epistemics, the institutions that steering capacity
is made of. In my model w/acc multiplies the effectiveness of everything
else, and its honest weakness is that alone it is slow.

Accelerate the steering and you get s/acc. Steerism in prose. Throttle
bounded by grip, re-measured at every corner. Maximum sustainable speed,
which is not the same as maximum speed, and is very much not zero speed.
The stopper deserves a concession too: stopping is a coherent response to
hazard. But run it in the model and watch what happens. Unilateral stopping
hands the wheel to the least careful driver on the road. You do not get a
parked world. You get someone else's world, decided from the passenger
seat. The simulator calls that outcome SHOTGUN, and the stopper preset
lands there 86 percent of the time.

## The model

I ported the race model to Python so the toy and the tests share equations.
Two policies drive a course of five corners. Speed compounds. Steering
accumulates from investment and from distance driven. Each corner draws a
control-loss event from the law above. Six outcomes: ARRIVED, CONVOY,
SHOTGUN, HELD, CRASHED, PILEUP.

Floor the throttle with token safety spend, the e/acc preset, and 61
percent of Monte Carlo runs end in CRASHED or PILEUP. Drive the envelope
rule, throttle equals grip times a margin, invest hard in grip, and the
plurality outcome is CONVOY: you arrive, together, a little later than the
reckless timeline and alive. The stopper watches someone else arrive.

Then I replaced the single rival with sixteen actors drawing throttle from
a distribution, because the real question was never my throttle. It was the
field's. A coordination dial kappa couples every actor toward the envelope
norm, and crashes cascade to coupled neighbours. Here is the theorem the
model was built to check: for an actor who has already done basic
diligence, a marginal unit of field-wide coordination buys more personal
survival than the same unit spent on private virtue. It passes at every
gridpoint on its stated domain, nine out of nine. And it has an honest
boundary that I refuse to hide: below basic diligence the inequality
fails. Buy your own brakes first. Then buy the treaty.

There is a third layer, because Wingston rejected the car metaphor as
presentation, and he was right to. Nobody eats an outcome distribution.
The Sustenance Ledger converts every race outcome into the only metric
that survives contact with a kitchen: hours of work per week to afford
food, shelter and energy, tracked for eight tribes from a salaried
professional in Amsterdam to a street vendor in Lagos to a commune that
mostly opted out of markets. Shelter is land and refuses to deflate.
Past sixty hours a week the market has failed you and dinner migrates to
non-market exchange: care, craft, mutual aid, verified-human work.

The proof table at the bottom of the instrument asks, for each tribe,
which worldview minimizes their worst decade. With the coordination dial
live, s/acc wins every row it does not tie. Force coordination to zero and
every single row becomes a tie. Read that carefully, because it is the
most important honest result in the toy: private virtue keeps your own
lane clean, and does almost nothing for anyone's kitchen. The s/acc claim
was never "be careful and you will be fine." It is "the throttle rule only
pays at field scale," which is an argument for treaties, standards bodies
and verification regimes, not for personal purity.

## The roads already ran this experiment

Now the part where the data gets a vote. The claim h = f(v/s) is not
about AI. It is about any transition. So it should already be visible in
the transitions we finished. I took five domains, all public data, fetch
scripts committed, fit windows and falsifiers frozen in the README before
the published run.

Roads first, because the metaphor is not a metaphor there. America put a
hundred times more miles under its wheels in 2019 than in 1921, and deaths
per mile fell about twenty-fold. The fatality rate tracks the steering
stack: licensing, the 1966 safety acts, belts, the 0.08 limit, electronic
stability control. In levels the steering index explains 93 percent of the
variance, so much that speed barely gets a word in, and I flag that
honestly: level fits on trending series are permissive. The strict test is
first differences, and there both terms carry signal. Speed changes matter,
p equals 0.016. Steering changes matter, p equals 0.045. The ratio is not
decoration on the road that named the theory.

Aviation, and here is a concession bigger than most manifestos ever make:
aviation votes against me and for the stoppers. The oversight stack, ICAO
to CRM to TCAS, tracks the collapse in fatal accidents per million flights
so completely that once you control for it, departure growth adds almost
nothing, and in first differences at annual frequency my steering term
goes silent too, p equals 0.59. Aviation reads as "s dominates, v is
noise." I keep it on the scoreboard because a theory that only cites
friendly domains is marketing.

Finance is the flagship, because finance gives what roads cannot: eighteen
countries, 145 years, 75 dated systemic crises in the Jorda-Schularick-
Taylor database. Credit growth is speed. An era-coded regulation index is
grip, and yes, that coding is coarse, the honesty notes say exactly how
coarse. First I reproduce the known result: credit booms predict crises.
Schularick and Taylor hold up. Then the addition: the steering term
improves the fit at p around four in a billion, and the single best
out-of-sample predictor, leave one decade out entirely, is the ratio
model. AUC 0.688 against 0.506 for credit growth alone. The quiet period
is the picture worth staring at: 1945 to 1972, capital controls and
financial repression everywhere, credit growing fast, and nearly zero
systemic crises anywhere in the panel. High v, higher s, quiet world.

Nuclear I refuse to fit. Seven decades, ten INES-4-class events, a
logistic regression on that would be numerology. As a case study it is
consistent: the decades with fast build-out and young regulators carry a
thirteen-fold higher event rate per reactor-year than the decades with
slow build-out and old regulators, and the rank correlation between v/s
and the event rate is 0.82. Consistent, I said. Not proof.

And AI. There is no outcome data for AI corners, and I will not pretend
otherwise. What I can compute is the same ratio, frontier training compute
growth from Epoch's public dataset over a steering proxy built from policy
counts and eval institutions, and place it on the same relative scale as
the finished domains. Two honest readings come out. First, AI's ratio in
2014 to 2016 spiked above the band where every historical domain's corners
bit. Second, and this one surprised me, on these crude proxies the ratio
has fallen since 2019, because policy counts and eval orgs grew faster
than frontier compute. Before anyone relaxes: a policy count is not policy
effectiveness, an eval org is not an eval regime with teeth, and nothing
in that chart measures whether the steering actually connects to the
wheels. The chart says the world is trying. It does not say the world is
steering.

## The psychohistory reading

This module lives in a psychohistory repository, so it owes the framework
a reading of itself, and the framework has one to give.

The race is a mean-field game, the same L5 machinery this project uses for
bank runs and forward guidance. Each lab best-responds to its expectation
of the field's throttle, and the field's throttle is the aggregate of
those best responses. That is a reflexive fixed-point problem, and it has
two self-consistent equilibria: everyone races because everyone expects a
race, or the field holds an envelope norm because deviating from a held
norm is visibly punished. The coordination dial kappa is not a policy
fantasy. It is the order parameter selecting between fixed points, and the
theorem check is a statement about which basin pays.

The flags themselves are attention objects. In the framework's terms, the
x/acc template is an existing attractor in identity space, which is why a
new position is cheaper to propagate as s/acc than as a paragraph.
Identity nouns add a reinforcing loop, since exiting an identity costs
more than changing vocabulary. This is the transport-and-drift layer
applied to the discourse itself, and it is also a warning label: the same
mechanics that spread a careful flag spread a careless one. The framework
files that under its dual-use notice, and so do I.

And the boundary the framework always draws applies here too. The
validation shows the envelope ratio organizes the past. The mean-field
layer shows why private virtue cannot organize the future alone. Neither
licenses a forecast of when any specific corner arrives. The skill horizon
on that question is short, and the honest output is the ratio, watched
continuously, not a date.

## What would change my mind

Falsifiers were frozen in the README before the run, and here they are in
prose. If the steering term had added nothing over speed in most of the
fittable domains, the envelope would be decoration and s/acc would lose
its empirical leg. That did not happen; it survived in two of three, with
aviation logged against. If steering alone had dominated everywhere and
speed never mattered, the stoppers would be right and I would say so.
That did not happen either; speed carries signal in roads and finance.
Going forward: show me a domain where disasters track v/s worse than v
alone out-of-sample, or show me the AI steering proxies rising while
actual verification capacity rots, and I will update in public, in this
repository, in the same tables.

## The call

So here is what I am asking, depending on which seat you are in.

If you build: publish your envelope. State your corner list, your grip
metrics, and the throttle rule that connects them. "We slow when X" is a
falsifiable safety culture. Vibes are not.

If you regulate: fund grip, not just brakes. Evals, incident channels,
verification regimes, owned compute, absorption floors. The quiet period
did not park the economy. It grew fast with its hands on the wheel.

If you write and argue: stop scoring the debate as gas versus brakes. The
axis that predicts the record is grip versus speed. Ask every accelerant
where the steering is, and ask every stopper whose hands they are leaving
on the wheel.

The engine is real. The corners are real. The data from the last century
says the ratio is what decides. Drive fast. Never faster than you can
steer.

*Wingston Sharon, 2026. Falsifiers, fit windows and code:
[`steering_envelope/`](https://github.com/wingie/psychohistory/tree/main/steering_envelope).
No part of this page waives the repository's
[dual-use notice](../ETHICS.md).*

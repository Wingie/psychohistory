# Concentration and recovery on the transport equation

n=40 topic nodes, random graph (p=0.15), D=0.05, dt=0.02, 6000 steps.
Total mass is the paper's conservation check. p_max and the Dirichlet
energy are the concentration observables. All three from one run.

| beta/D | mass err | p_max start -> end | Dirichlet start -> end | min p end | p_max doubles at |
|---|---|---|---|---|---|
| 0 | 1.1e-15 | 0.0273 -> 0.0250 | 2.23e-04 -> 3.21e-11 | 2.36e-02 | None |
| 20 | 4.4e-16 | 0.0273 -> 0.0250 | 2.23e-04 -> 4.80e-09 | 2.36e-02 | None |
| 40 | 8.9e-16 | 0.0273 -> 0.0271 | 2.23e-04 -> 8.96e-05 | 2.36e-02 | None |
| 50 | 4.4e-16 | 0.0273 -> 0.0764 | 2.23e-04 -> 4.40e-02 | 2.00e-02 | 1488 |
| 60 | 1.3e-14 | 0.0273 -> 0.1085 | 2.23e-04 -> 1.20e-01 | 1.67e-02 | 704 |
| 70 | 1.1e-14 | 0.0273 -> 0.1314 | 2.23e-04 -> 2.03e-01 | 1.43e-02 | 465 |
| 80 | 1.7e-14 | 0.0273 -> 0.1486 | 2.23e-04 -> 2.74e-01 | 1.25e-02 | 347 |
| 160 | 2.7e-15 | 0.0273 -> 0.2090 | 2.23e-04 -> 5.78e-01 | 6.25e-03 | 116 |
| 320 | 1.3e-15 | 0.0273 -> 0.2403 | 2.23e-04 -> 7.78e-01 | 3.13e-03 | 51 |
| 640 | 6.7e-16 | 0.0273 -> 0.2583 | 2.23e-04 -> 9.02e-01 | 1.56e-03 | 25 |

## Recovery against a moving reference

Kick of 1e-3 per node at step 200; separation from the UNPERTURBED
run of the same system; recovered when separation falls under 10% of
its initial value; window 1500 steps. CENSORED means not observed to
return inside the window, which is not the same as not returning.

| beta/D | norm | sep at kick | sep at window end | recovery step |
|---|---|---|---|---|
| 0 | l2 | 7.24e-03 | 4.15e-04 | 1003 |
| 0 | grad | 1.52e-02 | 1.96e-04 | 566 |
| 20 | l2 | 6.81e-03 | 1.00e-03 | CENSORED |
| 20 | grad | 1.53e-02 | 6.73e-04 | 909 |
| 80 | l2 | 7.06e-03 | 1.16e-01 | CENSORED |
| 80 | grad | 1.17e-02 | 3.00e-01 | CENSORED |
| 160 | l2 | 6.24e-03 | 4.52e-03 | CENSORED |
| 160 | grad | 1.49e-02 | 1.57e-02 | CENSORED |

## Finite-time fit of the peak on the focusing runs

beta/D = 160: fit on steps [108, 6000] gives T* = 11996, alpha = 0.12, log-resid 1.29e-02; p_max reaches 0.5 at step None.
beta/D = 640: fit on steps [23, 6000] gives
  p_max ~ C (T*-t)^-alpha on 0.05 < p_max < 0.5: T* = 11996, alpha = 0.03, log-resid 3.96e-03; p_max actually reaches 0.5 at step None.

## The window shrinks toward the focusing time

beta/D = 640 run, kick at later steps; p_max did not reach 0.5 inside the run, so every window ends at the run's end, step 6000. On this finite graph the peak grows and then slows toward a concentrated stationary state; the finite-time form is a continuum statement, and the fit above is the instrument to point at a real series, not a reading confirmed here.

| kick step | window | sep at kick | sep at end | recovery step |
|---|---|---|---|---|
| 200 | 5800 | 1.83e-02 | 8.40e-03 | CENSORED |
| 600 | 5400 | 1.51e-02 | 1.34e-02 | CENSORED |
| 1000 | 5000 | 1.63e-02 | 1.03e-02 | CENSORED |
| 1400 | 4600 | 1.42e-02 | 1.11e-02 | CENSORED |

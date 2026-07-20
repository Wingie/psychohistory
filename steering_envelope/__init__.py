"""Steering Envelope — a hazard model for technology transitions.

Python reference implementation of the s/acc "steering envelope" race model
(ported from the JS v0.2 artifact spec), extended with a mean-field N-actor
layer (`meanfield`), a society/tribes layer (`society`), and an empirical
validation suite (`validate/`) that tests the core structural claim against
public historical datasets.

Core hazard law: control-loss risk at a capability corner is logistic in the
ratio of deployment velocity to steering capacity,

    h = sigma( beta * ( (v * k) / (s * c0) - 1 ) )

The four positioning flags encoded alongside it:

    e/acc   maximize v unconditionally           (engine)
    d/acc   reallocate v toward defense          (armor)
    s/acc   constrain v <= f(s)                  (steering)  <- thesis under test
    w/acc   grow the judgment feeding s          (driver)
"""

from .model import (
    Corner,
    Course,
    RaceConfig,
    Outcome,
    hazard,
    speed,
    steer,
    run_race,
    monte_carlo,
    PRESETS,
)

__version__ = "0.2.0"

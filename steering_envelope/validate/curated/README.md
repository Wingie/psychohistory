# Curated tables: sources and honesty notes

These small hand-coded tables are the steering-capacity (`s`) proxies and
case-study inputs that no single machine-readable public dataset provides.
They are committed (unlike the raw downloads in `../data/`, which are
gitignored and regenerable via `datasets.py`). Every number here is either a
documented institutional date or an explicitly flagged order-of-magnitude
approximation. If you improve a coding, keep the pre-registered fit windows
in the main README unchanged or report the change.

## us_road_steering.csv

Major additions to US road-control capacity, coded 0.5 / 1.0 / 1.5 by scope.
Dates are standard institutional history: Uniform Vehicle Code (1926, FHWA
Highway History), spread of examined licensing by the mid-1930s (FHWA),
first BAC standards (1938, NSC/AMA recommendation), Interstate Highway Act
(1956), National Traffic and Motor Vehicle Safety Act and Highway Safety Act
(1966), FMVSS 208 belts (1968), NHTSA (1970), 55 mph limit (1974), MADD
(1980), National Minimum Drinking Age Act and first state belt-use law
(1984, NY), majority belt-use laws (~1990, IIHS state tables), dual airbags
(1998), .08 BAC (2000), ESC mandate FMVSS 126 (2012). The weights are a
judgment call; the fit is robust to reasonable re-weightings (checked in
`roads.py` with a +-50% weight jitter).

## aviation_steering.csv

Global commercial-aviation oversight milestones: Chicago Convention/ICAO
(1944), FAA (1958), NTSB (1967), CVR/FDR mandates (by 1968 in the US), GPWS
mandate (1974), CRM adoption dated to its introduction at United after
flight 173 (1981), TCAS II mandate (1993), EGPWS/CFIT work (1998), ICAO
USOAP audits (1999), IATA IOSA (2003), SMS/Annex 19 path (2010). Same
weight coding and jitter check as roads.

## finance_regulation_index.csv

An era-level regulation/repression index for the JST panel. Direction and
break years follow the financial-repression and liberalization literature
(Reinhart & Rogoff 2009; Abiad, Detragiache & Tressel 2010): minimal
pre-1914 regulation, interwar chaos, post-Depression re-regulation, the
Bretton Woods repression era (1945-72, the famous near-zero-crisis "quiet
period"), staged liberalization from 1973, the light-touch peak before
2008, Basel III afterwards. HONESTY NOTE: this is one global era coding,
not a country-level index; country-level liberalization indices exist only
post-1973. The LR tests in `finance.py` therefore measure whether even this
coarse an s-proxy adds signal over credit growth — a deliberately hard test
for the steering term.

## nuclear.csv

Decade-level case study, small-N by design. INES>=4-class events from
standard references (Kyshtym 1957, Windscale 1957, SL-1 1961, Lucens 1969,
Saint-Laurent 1969 and 1980, Three Mile Island 1979, Chernobyl 1986,
Tokaimura 1999, Fukushima 2011). Reactor-years and capacity additions are
order-of-magnitude reads of IAEA PRIS aggregates and OWID nuclear data.
`s_regulator` codes regulator maturity (pre-NRC, post-TMI reforms, WANO
1989, post-Fukushima). No formal fit is performed on this table — 7 rows,
10 events — only rate comparisons with wide priors, as the main README
pre-registers.

## ai_steering.csv

Order-of-magnitude ONLY, clearly flagged. `policy_cum` tracks the OECD.AI
national policy database's growth (~zero in 2015 to ~1000 initiatives by
2024); `eval_orgs_cum` counts dedicated frontier-evaluation institutions
(ARC Evals/METR 2022, UK AI Safety Institute 2023, US AISI 2023, and
successors); `aiid_incidents` approximates yearly new records in the AI
Incident Database + AIAAIC. These series enter only the leading-indicator
ratio chart (`ai_proxy.py`), never a fitted hazard: there is no outcome
data for AI corners yet, and the module says so.

## Licenses

- JST Macrohistory Database: free for non-commercial research use, cite
  Jorda, Schularick & Taylor (2017).
- Wikipedia table (FHWA/NHTSA series): CC BY-SA 4.0.
- Our World in Data: CC BY 4.0.
- World Bank Open Data: CC BY 4.0.
- Epoch AI notable models: CC BY 4.0.
- This directory's curated codings: CC BY 4.0, cite this repository.

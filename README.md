# Phase API — RIS Companion Artifacts
[![Validate ERDs](https://github.com/zeropilot-corp/phase-api-ris/actions/workflows/validate.yml/badge.svg)](https://github.com/zeropilot-corp/phase-api-ris/actions/workflows/validate.yml)
[![License: CC0-1.0](https://img.shields.io/badge/Schema%20%26%20Descriptors-CC0--1.0-lightgrey)](LICENSE)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue)](LICENSE)
[![Submitted: IEEE AP Magazine](https://img.shields.io/badge/Submitted-IEEE%20AP%20Magazine%202026-orange)]()
[![ETSI ISG RIS](https://img.shields.io/badge/ETSI-ISG%20RIS%20Traceable-green)]()

**The Phase API** is an open, non-normative hardware-behavior interface for 6G Reconfigurable
Intelligent Surfaces — comprising the **Element Response Descriptor (ERD)** and the
**Spatial Valid Range (SVR)** — that separates aperture synthesis from unit-cell realization
and gives the layers above a machine-consumable hardware prior to facilitate integration of the RIS in a 6G mobile network.

**Author:** R. D. Javor, Founder, ZeroPilot Corporation  
**Companion paper:** *"The Phase API — A Hardware-Behavior Interface for Integrating RIS into
Signal-Processing and Network Layers of 6G,"* submitted to *IEEE Antennas and Propagation
Magazine*, 2026. DOI: forthcoming.

**Keywords:** `RIS` · `Phase API` · `ERD` · `SVR` · `6G` · `reflectarray` · `ETSI` ·
`GS-RIS-008` · `aperture-synthesis` · `unit-cell` · `beamforming` · `mmWave` · `28GHz`

---

## Key Result

In a controlled hardware-swap demonstration on a fixed 28 GHz aperture, holding the
Layer-1 phase map invariant while swapping only the ERD — from a 1-bit PIN-diode descriptor
to a varactor-tuned continuous descriptor — changes realized gain (−4.1 dB vs. −0.7 dB) and
EVM (11.5% vs. 7.9%) **exactly as the descriptor fields predict**, without re-deriving the
aperture synthesis.

This is a descriptor-level, array-factor demonstration of the interface mechanism. It is not
a full-wave-validated electromagnetic study or hardware prototype validation. Full-wave and
measured ERD population is explicitly identified as the natural next step for an
implementation-focused follow-on.

---

## Overview

This repository is the companion artifact package for the paper above. The paper proposes the
Phase API — comprising two machine-consumable artifacts, the ERD and the SVR — that the 6G
RIS community can adopt and profile to facilitate RIS integration across antenna, signal-
processing, and network layers.

Together, ERD and SVR make explicit, declarable, and testable a separation that reflectarray
and RIS engineers have long maintained implicitly:

1. Synthesizing the aperture-level phase distribution required to produce a desired beam
2. Realizing that distribution in hardware using a specific unit-cell implementation

**Element Response Descriptor (ERD)** — A design-time, machine-consumable behavioral
component datasheet for a RIS unit cell. It declares what the unit cell *does* at the Phase
API boundary (realized phase range, amplitude variation, coupling, calibration) without
exposing internal geometry, substrate stack-up, or bias-circuit details. From a signal-
processing perspective, the ERD is a declared response prior that beamforming, codebook,
and channel-estimation algorithms can consume to reduce in-band pilot overhead.

**Spatial Valid Range (SVR)** — The declared angular operating domain within which a RIS
panel's incident and redirected waves can be modeled with scalar or vector phase coefficients
and managed with practical runtime control complexity. From a network perspective, the SVR
is an orchestration and handoff boundary governing the runtime **stay → correct → hand off
→ reject** decision.

**Scope of this work** — This is a perspective and tutorial contribution proposing an open
interface specification. The contribution is an interface formalism rather than new
electromagnetics. It is framed as a perspective and tutorial rather than a measurement study,
and the specification is proposed as open and non-normative — designed to feed into, not
replace, the ETSI ISG RIS framework.

**A call for the decade ahead** — The reflectarray community has spent three decades mastering
how to make a surface deliver a desired phase. The next ten years ask that we declare that
behavior in a form the network can consume. By treating the ERD and SVR as first-class
deliverables shipped alongside the hardware, antenna engineers give the layers above a
structured hardware prior — the foundation on which in-band pilot and CSI dependence can
be reduced, rather than indefinitely scaled, as element counts grow.

---

## Repository Contents


```
phase-api-ris/
├── README.md ← This file
├── LICENSE ← CC0-1.0 (schema/docs) + MIT (code)
├── CONTRIBUTING.md ← Community profiling and ERD submission guidelines
├── paper/
│ ├── PhaseAPIRIS_MainPaper.pdf ← Main paper (perspective/tutorial) — forthcoming post-acceptance
│ └── PhaseAPIRIS_Supplementary.pdf← Supplementary material (S-I – S-X) — forthcoming
├── schema/
│ ├── erd.schema.json ← Non-normative JSON schema for the ERD
│ ├── erd_pin_28ghz.json ← Populated ERD: 1-bit PIN-diode hardware class
│ └── erd_varactor_28ghz.json ← Populated ERD: varactor-tuned continuous hardware class
├── experiments/
│ ├── exp_hardware_swap.py ← Hardware-swap invariance Monte Carlo [forthcoming]
│ ├── exp_wideband_squint.py ← Wideband squint profile vs. ERD frequency grid [forthcoming]
│ ├── exp_coupling_robustness.py ← Inter-element coupling robustness sweep [forthcoming]
│ ├── exp_evm_gsr008.py ← EVM proxy mapped to GS RIS 008 validation [forthcoming]
│ ├── validate_erd.py ← Reference ERD validation script
│ ├── run_all_experiments.sh ← Reproduce all supplement experiments [forthcoming]
│ └── expected_results.json ← Reference outputs for CI validation fixture 

```
> **Note on experiment scripts:** Full Python experiment scripts reproducing the supplement
> results are forthcoming. The supplementary material (Sections S-III – S-VIII) provides
> complete methodology, equations, and parameter tables sufficient for independent
> reproduction. Scripts will be added at or before paper publication.

---

## Quickstart

### Requirements
```bash
git clone https://github.com/zeropilot-corp/phase-api-ris.git
cd phase-api-ris
pip install numpy scipy matplotlib jsonschema   # Python 3.9+ recommended
```

No hardware or full-wave solver is required. All experiments use the array-factor model with
statistically representative ERD fields, as declared in the supplement.

### Validate an ERD

```bash
python experiments/validate_erd.py schema/erd_pin_28ghz.json
python experiments/validate_erd.py schema/erd_varactor_28ghz.json
```

### Run All Supplement Experiments

```bash
cd experiments
bash run_all_experiments.sh
```

Or run individually:

```bash
python exp_hardware_swap.py       # Monte Carlo hardware-swap invariance
python exp_wideband_squint.py     # Beam squint vs. frequency 26.5–29.5 GHz
python exp_coupling_robustness.py # Pointing error vs. coupling |S| sweep
python exp_evm_gsr008.py          # EVM proxy → GS RIS 008 ATP result
```

### Array Configuration (Fixed Across All Experiments)

| Parameter | Value |
|---|---|
| Array size | 10×10 (N = 100 elements) |
| Design frequency | 28 GHz |
| Element spacing dx, dy | 0.5λ = 5.36 mm |
| Desired beam direction | θ = 30°, φ = 0° (elevation plane) |
| Polarization | Linear x-pol |
| Incident illumination | Normal incidence (0°), within SVR core |
| Layer-1 phase map | Progressive phase per Eq. (1) — never re-derived across hardware swaps |

---

## ERD Field Reference

The ERD is a declared interface artifact — a structured behavioral specification that a
hardware vendor can publish and a controller or signal-processing algorithm can consume
without knowledge of internal geometry.

| ERD Field | Type | Units | Phase API Role |
|---|---|---|---|
| `realizedPhaseRange` | float[2] | degrees [min, max] | Declares achievable phase extent |
| `phaseQuantizationResolution` | float | degrees | State granularity — determines quantization residual |
| `amplitudeVariation` | float | dB peak-to-peak | Aperture efficiency loss predictor |
| `amplitudePhaseCoupling` | float | dB/rad | Command realization error / runtime correction budget |
| `nearestNeighborCoupling` | float | dB (\|S\|) | Coupling metadata — declared, not hidden in synthesis |
| `operatingFrequencyGrid` | float[] | GHz | Core field enabling wideband squint prediction |
| `perStateInsertionLoss` | float[] | dB per state | Per-state gain contribution to link budget |
| `phaseErrorRms` | float | degrees (1σ Gaussian) | State-realization tolerance — feeds EVM budget |
| `amplitudeErrorRms` | float | dB (1σ) | Amplitude tolerance — feeds aperture efficiency |
| `polarization` | string | e.g. `linear-x`, `dual`, `RHCP` | Operating polarization declaration |
| `calibrationUncertaintyBudget` | float | degrees (1σ) | Residual implementation error — performance confidence margin |
| `temperatureDrift` | float | degrees/°C | Environmental stability declaration |
| `stateTransitionTiming` | float | µs | Controller scheduling constraint |
| `svrCoreAngularLimits` | object | degrees (inc, scat bounds) | Core region: scalar/vector control sufficient |
| `svrMarginalAngularLimits` | object | degrees | Marginal region: apply corrections, prepare handoff |
| `widebandSquintCharacterization` | float | degrees/GHz | Squint profile across frequency grid |
| `hardwareClass` | string | e.g. `PIN-binary`, `varactor-continuous` | Runtime control object selector |

> **Production note:** A production ERD should populate `operatingFrequencyGrid`,
> `perStateInsertionLoss`, `nearestNeighborCoupling`, and SVR fields from full-wave
> (HFSS/CST) unit-cell solves and GS RIS 008 black-box measurements. The populated example
> ERDs in `schema/` use statistically representative values consistent with the
> perspective/tutorial scope of this work.

### Blank ERD Template

Copy-paste starting point for vendors publishing a behavioral ERD without disclosing geometry,
substrate stack-up, or bias-circuit details:

```json
{
  "erdVersion": "1.0",
  "hardwareClass": "",
  "vendor": "",
  "partNumber": "",
  "realizedPhaseRange": [0.0, 360.0],
  "phaseQuantizationResolution": null,
  "amplitudeVariationdB": null,
  "amplitudePhaseCouplingdBperRad": null,
  "nearestNeighborCouplingdB": null,
  "operatingFrequencyGridGHz": [],
  "perStateInsertionLossdB": [],
  "phaseErrorRmsDeg": null,
  "amplitudeErrorRmsdB": null,
  "polarization": "",
  "calibrationUncertaintyBudgetDeg": null,
  "temperatureDriftDegPerC": null,
  "stateTransitionTimingUs": null,
  "svrCoreAngularLimits": { "thetaIncidentMaxDeg": null, "thetaScatteredMaxDeg": null },
  "svrMarginalAngularLimits": { "thetaIncidentMaxDeg": null, "thetaScatteredMaxDeg": null },
  "widebandSquintDegPerGHz": null,
  "notes": ""
}
```

---

## GS RIS 008 Traceability

Each ERD-declared field maps to a predicted link-level impact, network/signal-processing
relevance, and a GS RIS 008 verification method. This table is a living community reference —
contributions that extend or refine mappings are welcome via pull request.

| ERD Declaration | What It Predicts | Network / SP Relevance | GS RIS 008 Verification |
|---|---|---|---|
| Phase Quantization | Quantization residual | Codebook resolution limits | Phase-state measurement |
| Phase Range | Interpolation / realization residual | Beam accuracy and EVM | State sweep, far-field test |
| Amplitude Variation | Aperture efficiency loss | Link-budget prediction | Amplitude characterization |
| Amplitude–Phase Coupling | Command realization error | Runtime correction requirements | State-sweep characterization |
| Calibration Budget | Residual implementation error | Performance confidence margin | Calibration verification |
| SVR Angular Limits | Valid operating domain | Stay → Correct → Hand Off → Reject | Angular scan testing |
| Frequency Grid | Wideband squint profile | Multi-band scheduling | Per-frequency far-field scan |
| Nearest-Neighbor Coupling | Beam pointing stability | Correction model selection | Coupling characterization |

**ETSI ISG RIS references:** GR RIS 003 (modeling) · GR RIS 004 (implementation) ·
GR RIS 007 (near-field) · GS RIS 008 (standardized testing)

---

## Supplement Experiment Summary

| Section | What Is Tested | Key Result |
|---|---|---|
| S-III – S-IV | Hardware-Swap Invariance: hold Layer-1 map fixed, swap PIN ERD → varactor ERD | Geometry, beam, and Layer-1 map invariant. Gain −4.1 dB vs. −0.7 dB; pointing error 0.5° vs. 0.0° change only as declared by ERD |
| S-V | Coupling Robustness: sweep \|S\| from 0.0 to 0.20 (−14 dB) | Beam pointing invariant across full sweep; coupling marginally degrades gain ~0.1 dB but does not shift beam direction |
| S-VIII | SVR Regime Transitions: map incident/redirected angles to core/marginal/outside-SVR zones | Compute regime and controller action (stay/correct/hand off/reject) follow directly from declared SVR limits |
| S-VI | EVM → GS RIS 008: decompose per-element phase-error budget to EVM proxy ATP result | PIN ERD EVM 11.5% approaches 64-QAM-class threshold (12.5%); Varactor ERD EVM 7.9% retains margin |

### Model Assumptions and Stated Limitations

The demonstration deliberately uses an array-factor model with statistically representative
ERD fields. It is a **descriptor-level interface interoperability study**, not a full-wave-
validated electromagnetic study or hardware prototype validation. The following assumptions apply:

- Array-factor model with element-pattern roll-off omitted
- Frequency-dispersion and coupling models are phenomenological surrogates for measured unit-cell data
- Mutual coupling matrix truncated to nearest neighbors only; E- and H-plane coupling assumed identical
- EVM metric is a phase-error-driven proxy, not a modulated-waveform link simulation
- ERD fields are statistically representative values; a production ERD would populate from HFSS/CST solves and GS RIS 008 black-box measurements

These simplifications do not affect the structural conclusion: a single aperture synthesis
survives a change of hardware class through the ERD without re-derivation.

---

## ETSI ISG RIS Traceability Map

The ERD and SVR are designed to feed into — not replace — the ETSI ISG RIS framework.

| ETSI Functional Area | Representative ERD Fields | Phase API Role |
|---|---|---|
| Modeling (GR RIS 003) | Realized Phase Range, Amplitude Variation, Wideband Squint | Describes achievable electromagnetic behavior |
| Implementation (GR RIS 004) | Phase Quantization, Nearest-Neighbor Coupling | Describes hardware realization constraints |
| Near-Field Behavior (GR RIS 007) | Amplitude–Phase Coupling, Nearest-Neighbor Coupling | Captures local interaction effects and correction requirements |
| Testing/Verification (GS RIS 008) | Calibration Uncertainty, SVR Angular Limits | Supports validation, certification, and deployment readiness |

---

## CSI and Pilot Design Note

CSI and pilot design lie **above** the Phase API boundary. The Phase API does not prescribe
an in-band pilot waveform, a RIS training sequence, or a cascaded-channel estimator — it
supplies the hardware-side descriptor that such algorithms consume.

In CSI terminology, the ERD acts as a declared prior or constraint on the RIS response, while
the SVR defines the angular domain over which that prior is valid. Channel-estimation and pilot
methods remain free to choose their own training protocol; they no longer need to treat the RIS
hardware response as an undocumented ideal phase surface.

---

## Future Work and Call to the Community

The Phase API does not itself estimate a channel, predict a phase map, or orchestrate a handoff
— it declares the hardware truth on which those activities depend. Building the control planes
that exploit that declared prior is the work of the decade ahead.

Natural next steps, open to all communities:

- **Full-wave / measured ERD population** *(antenna engineers)* — Populate ERD fields
  (frequency grid, per-state insertion loss, coupling, SVR limits) from HFSS/CST unit-cell
  solves and GS RIS 008 black-box measurements; characterize near-field behavior; generalize
  to transmitting and refracting surfaces.
- **Signal-processing integration** *(communications researchers)* — Incorporate ERD-declared
  priors and SVR validity constraints into beamforming codebooks, cascaded-channel estimators,
  and pilot-design frameworks so hardware behavior is exploited rather than rediscovered at runtime.
- **Network-scale SVR handoff** *(network researchers)* — Evaluate predictive panel handoff at
  the marginal SVR boundary across multi-panel deployments.
- **Community ERD profiling** — Grow an open library of populated ERDs across hardware classes,
  frequency bands, array geometries, and coupling models via this repository.

None of these require the network's permission to begin — all of them begin on the antenna
engineer's bench. Contributions in any of these directions are welcome (see Contributing below).

---

## Citation

**IEEE format:**

> R. D. Javor, "The Phase API — A Hardware-Behavior Interface for Integrating RIS into
> Signal-Processing and Network Layers of 6G," *IEEE Antennas and Propagation Magazine*,
> submitted 2026.

**BibTeX:**

```bibtex
@article{javor2026phaseapi,
  author  = {Javor, R. D.},
  title   = {The {Phase API} --- A Hardware-Behavior Interface for Integrating {RIS}
             into Signal-Processing and Network Layers of {6G}},
  journal = {IEEE Antennas and Propagation Magazine},
  year    = {2026},
  note    = {Submitted},
  keywords= {RIS, reflectarray, Phase API, ERD, SVR, 6G, ETSI, GS-RIS-008,
             aperture synthesis, unit cell, beamforming}
}
```

---

## Contributing

This repository is an open community profiling artifact. Contributions are welcome in the
following areas:

- **ERD submissions** — Submit a populated ERD JSON for a hardware class not yet represented
  (see `schema/erd_pin_28ghz.json` as a template)
- **Traceability extensions** — Propose additions or refinements to the GS RIS 008 traceability
  table via pull request
- **Experiment extensions** — Additional hardware classes, array geometries, frequency bands,
  or coupling models
- **Schema evolution** — Proposed new ERD fields with rationale and ETSI traceability mapping

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for submission guidelines and ERD field naming
conventions.

---

## License

A split license model applies.

**Part A — Schema, field names, documentation, and example descriptors:**
Released under [CC0 1.0 Universal (Public Domain)](https://creativecommons.org/publicdomain/zero/1.0/)
to support royalty-free community adoption and profiling. This covers:
- `schema/erd.schema.json`
- `schema/erd_pin_28ghz.json`, `schema/erd_varactor_28ghz.json`
- All documentation text including `README.md` and `CONTRIBUTING.md`

**Part B — Reference validation/parsing code:**
Released under the [MIT License](LICENSE).

> **Scope limitation:** This dedication and license apply **only** to the schema, field names,
> documentation, example descriptors, and non-normative reference code described above.
> They do **not** dedicate, license, or grant any rights to any physical RIS implementation,
> unit-cell design, controller architecture, calibration apparatus, or manufacturing method,
> all of which are expressly reserved.

See [LICENSE](LICENSE) for full text.

---

## Acknowledgements

The reflectarray lineage underpinning this work traces to the early 1990s. Key foundational
references are cited in the paper: Javor, Wu & Chang (1995); Pozar & Metzler (1993);
Huang & Encinar (2007); Hum & Perruisseau-Carrier (2014).

The author thanks the ETSI ISG RIS working group for the standardization framework —
GR RIS 003, GR RIS 004, GR RIS 007, and GS RIS 008 — into which the Phase API specification
is designed to integrate.

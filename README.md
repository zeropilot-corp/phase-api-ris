# Phase API — Companion Artifact Repository

The Phase API is an open, non-normative hardware-behavior interface for 6G Reconfigurable Intelligent Surfaces — comprising the **Electromagnetic Response Descriptor (ERD)** and the **Spatial Validity Region (SVR)** — that separates aperture synthesis from unit-cell realization and gives the layers above a machine-consumable hardware prior.

**R. D. Javor** — Founder, ZeroPilot Corporation

> **Article type:** Perspective and tutorial contribution that proposes an open interface specification. This work defines and explains the Phase API for the 6G RIS ecosystem; the accompanying demonstration is a descriptor-level, array-factor interoperability study intended to make the specification concrete, not a full-wave-validated electromagnetic study or hardware prototype validation. The ERD and SVR are proposed as open, non-normative specifications designed to feed into — not replace — the ETSI ISG RIS framework.

---

## Overview

This repository is the companion artifact package for the paper:

> **"Electromagnetic Response Descriptors, Spatial Validity Regions, and the Phase API: An Antenna-Domain Interface for Reconfigurable Intelligent Surfaces in 6G"**
> R. D. Javor, ZeroPilot Corporation, 2026.

The paper proposes an open, non-normative interface specification — the **Phase API** — comprising two machine-consumable artifacts, the **Electromagnetic Response Descriptor (ERD)** and the **Spatial Validity Region (SVR)**, that the 6G RIS community can adopt and profile to facilitate RIS integration. Together they make explicit, declarable, and testable a separation that reflectarray and Reconfigurable Intelligent Surface (RIS) engineers have long maintained implicitly: (1) synthesizing the aperture-level phase distribution required to produce a desired beam, and (2) realizing that distribution in hardware using a specific unit-cell implementation.

- **Electromagnetic Response Descriptor (ERD)** — A design-time, machine-consumable behavioral component datasheet for a RIS unit cell. It declares what the unit cell *does* at the Phase API boundary (realized phase range, amplitude variation, coupling, calibration) without exposing internal geometry, substrate stack-up, or bias-circuit details. From a signal-processing perspective, the ERD is a declared response prior/constraint that beamforming, codebook, and channel-estimation algorithms can consume to reduce in-band pilot overhead.
- **Spatial Validity Region (SVR)** — The declared angular operating domain within which a RIS panel's incident and redirected waves can be modeled with scalar or vector phase coefficients and managed with practical runtime control complexity. From a network perspective, the SVR is an orchestration and handoff boundary — governing the runtime "stay / correct / hand off / reject" decision.

Together, ERD and SVR define the **Phase API**: a named, enforceable contract between the aperture synthesis layer (Layer-1 phase map) and the unit-cell realization layer (hardware), separating what the surface must do from how a specific hardware platform does it. ERD fields are explicitly traceable to ETSI ISG RIS modeling, implementation, near-field, and test concepts, including GS RIS 008 test categories.

**Scope of this work:** This is a perspective and tutorial contribution that proposes an open interface specification for the 6G RIS ecosystem — antenna engineers, hardware vendors, controller teams, network operators, test laboratories, and standards participants. The contribution is an interface formalism rather than new electromagnetics: the ERD turns implicit unit-cell behavior into a declarable, machine-consumable artifact; the SVR turns operating validity into a declared angular condition; and the Phase API turns the boundary between them into an enforceable contract. It is framed as a perspective and tutorial rather than a measurement study, and the specification is proposed as open and non-normative — designed to feed into, not replace, the ETSI ISG RIS framework.

**Headline result:** In a controlled hardware-swap demonstration on a fixed 28 GHz aperture, holding the Layer-1 phase map invariant while swapping only the ERD from a 1-bit PIN-diode descriptor to a varactor-tuned continuous descriptor changes realized gain (−4.1 dB vs. −0.7 dB) and EVM (11.5% vs. 7.9%) exactly as the descriptor fields predict — without re-deriving the aperture synthesis. This is a descriptor-level, array-factor demonstration of the interface mechanism, not a full-wave-validated electromagnetic study.

**A call for the decade ahead:** The reflectarray community has spent three decades mastering how to make a surface deliver a desired phase; the next ten years ask that we *declare* that behavior in a form the network can consume. By treating the ERD and SVR as first-class deliverables shipped alongside the hardware — a behavioral datasheet with its conditions of validity — antenna engineers give the layers above a structured hardware prior, the foundation on which the next decade can *reduce*, rather than indefinitely scale, in-band pilot and CSI dependence as element counts grow. This package is offered to help the antenna, signal-processing, and network communities begin that work now.

**Keywords:** `ETSI-RIS` `Phase-API` `ERD` `SVR` `6G` `RIS` `reflectarray` `GS-RIS-008` `aperture-synthesis` `unit-cell` `beamforming` `mmWave` `28GHz`

---

## Repository Contents

```
phase-api-ris/
│
├── README.md                             ← This file
│
├── paper/
│   ├── Phase_API_RIS_Main_Paper.pdf      ← Main paper (perspective/tutorial)
│   └── Phase_API_RIS_Supplementary.pdf   ← Supplementary material (S-I … S-X)
│
├── schema/
│   ├── erd.schema.json                   ← Non-normative JSON Schema (draft-07) for the ERD
│   ├── erd_pin_28ghz.json                ← Populated ERD: 1-bit PIN-diode hardware class
│   └── erd_varactor_28ghz.json           ← Populated ERD: varactor-tuned continuous hardware class
│
├── experiments/
│   ├── exp_hardware_swap.py              ← Hardware-swap invariance (Monte Carlo)
│   ├── exp_wideband_squint.py            ← Wideband profile / ERD frequency grid
│   ├── exp_coupling_robustness.py        ← Inter-element coupling robustness sweep
│   └── exp_evm_gsr008.py                 ← EVM proxy mapped to GS RIS 008
│
├── validation/
│   ├── validate_erd.py                   ← Reference ERD validation script (Draft7Validator)
│   ├── run_all_experiments.sh            ← Reproduce all supplement experiments
│   └── expected_results.json             ← Reference outputs for CI validation fixture
│
└── CONTRIBUTING.md                       ← Community profiling and ERD submission guidelines
```

---

## Quickstart

### Requirements

```bash
pip install numpy scipy matplotlib jsonschema
```

Python 3.9+ recommended. Consistent with the perspective and tutorial scope of this article, no hardware or full-wave solver is required — all experiments use the array-factor model with statistically representative ERD fields, as declared in the supplement.

### Validate ERD Schemas

```bash
python validation/validate_erd.py schema/erd_pin_28ghz.json schema/erd_varactor_28ghz.json
```

### Run All Supplement Experiments

```bash
cd experiments/
bash ../validation/run_all_experiments.sh
```

Or run individually:

```bash
python exp_hardware_swap.py        # Monte Carlo hardware-swap invariance
python exp_wideband_squint.py      # Beam squint vs. frequency (26.5–29.5 GHz)
python exp_coupling_robustness.py  # Pointing error vs. coupling |S| sweep
python exp_evm_gsr008.py           # EVM proxy → GS RIS 008 ATP result
```

### Array Configuration

All experiments use the following fixed geometry (never re-derived across hardware swaps), matching the paper's worked example (Section VI) and supplement Section S-II:

| Parameter | Value |
|---|---|
| Array size | 10 × 10 (N = 100 elements) |
| Design frequency | 28 GHz |
| Element spacing (dx = dy) | 0.5 λ ≈ 5.36 mm |
| Desired beam direction | θ = 30°, φ = 0° (elevation plane) |
| Polarization | Linear (x-pol) |
| Incident illumination | Normal incidence (0°), within SVR core |
| Layer-1 phase map | Progressive phase per Eq. (1) |

---

## ERD Field Reference

The ERD is a declared interface artifact — a structured behavioral specification that a hardware vendor can publish and a controller or signal-processing algorithm can consume without knowledge of internal geometry. The table below lists ERD fields, their types, units, and roles at the Phase API boundary.

| ERD Field | Type | Units | Phase API Role |
|---|---|---|---|
| `realized_phase_range` | float[2] | degrees [min, max] | Declares achievable electromagnetic phase extent |
| `phase_quantization_resolution` | float | degrees | State granularity; determines quantization residual. Use 0.0 for continuous hardware. |
| `amplitude_variation_dB` | float | dB (peak-to-peak across states) | Aperture efficiency loss predictor |
| `amplitude_phase_coupling_dB_per_rad` | float | dB/rad | Command realization error; runtime correction budget |
| `nearest_neighbor_coupling_dB` | float | dB (\|S\| magnitude) | Coupling metadata; declared at the Phase API boundary, not hidden in synthesis |
| `operating_frequency_grid_GHz` | float[] | GHz | Core field; enables wideband squint prediction |
| `per_state_insertion_loss_dB` | float[] | dB (per state) | Per-state gain contribution to link budget |
| `phase_error_rms_deg` | float | degrees (1σ Gaussian) | State-realization tolerance; feeds EVM budget |
| `amplitude_error_rms_dB` | float | dB (1σ) | Amplitude tolerance; feeds aperture efficiency |
| `polarization` | string | e.g. "linear-x", "dual", "RHCP" | Operating polarization declaration |
| `calibration_uncertainty_budget_deg` | float | degrees (1σ) | Residual implementation error; performance confidence margin |
| `temperature_drift_deg_per_C` | float | degrees/°C | Environmental stability declaration |
| `state_transition_timing_us` | float | μs | Controller scheduling constraint |
| `svr_core_angular_limits` | object | degrees (θ_inc, θ_scat bounds) | SVR core region: scalar/vector control sufficient |
| `svr_marginal_angular_limits` | object | degrees | SVR marginal region: apply corrections, prepare predictive handoff |
| `wideband_squint_deg_per_GHz` | float | degrees per GHz | Squint rate across the frequency grid |
| `hardware_class` | string | e.g. "PIN-binary", "varactor-continuous" | Runtime control object selector |

> **Note:** A production ERD should populate the `operating_frequency_grid_GHz`, `per_state_insertion_loss_dB`, `nearest_neighbor_coupling_dB`, and `svr_*` fields from full-wave (HFSS/CST) unit-cell solves and GS RIS 008 black-box measurements. Consistent with the perspective and tutorial scope of this article, the populated example ERDs in `schema/` use statistically representative values; populating them from full-wave solves or measurements is identified as the natural next step for an implementation-focused follow-on.

---

## Blank ERD Template (JSON)

Hardware vendors can use this template as a copy-paste starting point for publishing a behavioral Electromagnetic Response Descriptor (ERD) without disclosing geometry, substrate stack-up, or bias-circuit details. Signal-processing teams can use it as the hardware-side prior interface for channel estimation and beamforming.

```json
{
  "erd_version": "1.0",
  "hardware_class": "",
  "vendor": "",
  "part_number": "",
  "realized_phase_range": [0.0, 360.0],
  "phase_quantization_resolution": null,
  "amplitude_variation_dB": null,
  "amplitude_phase_coupling_dB_per_rad": null,
  "nearest_neighbor_coupling_dB": null,
  "operating_frequency_grid_GHz": [],
  "per_state_insertion_loss_dB": [],
  "phase_error_rms_deg": null,
  "amplitude_error_rms_dB": null,
  "polarization": "",
  "calibration_uncertainty_budget_deg": null,
  "temperature_drift_deg_per_C": null,
  "state_transition_timing_us": null,
  "svr_core_angular_limits": {
    "theta_incident_max_deg": null,
    "theta_scattered_max_deg": null
  },
  "svr_marginal_angular_limits": {
    "theta_incident_max_deg": null,
    "theta_scattered_max_deg": null
  },
  "wideband_squint_deg_per_GHz": null,
  "notes": ""
}
```

---

## GS RIS 008 Traceability

The following table maps each ERD-declared field to its predicted link-level impact, network/signal-processing relevance, and GS RIS 008 verification method. This table is intended as a living community reference; contributions that extend or refine mappings are welcome via pull request.

| ERD Declaration | What It Predicts | Network / Signal-Processing Relevance | GS RIS 008 Verification Method |
|---|---|---|---|
| Phase Quantization | Quantization residual | Codebook resolution limits | Phase-state measurement |
| Phase Range / Interpolation | Realization residual | Beam accuracy and EVM | State sweep + far-field test |
| Amplitude Variation | Aperture efficiency loss | Link-budget prediction | Amplitude characterization |
| Amplitude–Phase Coupling | Command realization error | Runtime correction requirements | State-sweep characterization |
| Calibration Budget | Residual implementation error | Performance confidence margin | Calibration verification |
| SVR Angular Limits | Valid operating domain | Stay / Correct / Hand Off / Reject decision | Angular scan testing |
| Frequency Grid | Wideband squint profile | Multi-band scheduling | Per-frequency far-field scan |
| Nearest-Neighbor Coupling | Beam pointing stability | Correction model selection | Coupling characterization |

> **ETSI ISG RIS reference documents:** GR RIS 003 (modeling), GR RIS 004 (implementation), GR RIS 007 (near-field), GS RIS 008 (standardized testing).

---

## Supplement Experiment Summary

The supplementary material provides reproducible experiments that stress-test the Phase API boundary using the array-factor model with statistically representative ERD fields. All assumptions are stated explicitly so that results are reproducible and their limits are clear.

| Section | What Is Tested | Key Result |
|---|---|---|
| **S-III / S-IV** Hardware-Swap Invariance | Hold Layer-1 map fixed; swap PIN ERD ↔ varactor ERD | Geometry, beam, and Layer-1 map are invariant. Gain (−4.1 dB vs. −0.7 dB) and pointing error (0.5° vs. 0.0°) change only as declared by the ERD |
| **S-V** Coupling Robustness | Sweep nearest-neighbor coupling \|S\| from 0.0 to 0.20 (−∞ to −14 dB) | Beam pointing invariant across full sweep; coupling marginally degrades gain (~0.1 dB) but does not shift beam direction |
| **S-VI** EVM → GS RIS 008 | Decompose per-element phase-error budget to EVM proxy (ATP result) | PIN ERD: EVM = 11.5% (approaches 64-QAM-class threshold of 12.5%); Varactor ERD: EVM = 7.9% (retains margin for higher-order modulation) |
| **S-VIII** SVR Regime Transitions | Map incident/redirected angles to core / marginal / outside-SVR zones | Compute regime and controller action (stay / correct / hand off / reject) follow directly from declared SVR limits |

### Model Assumptions and Stated Limitations

Consistent with the perspective and tutorial scope of this article, the demonstration deliberately uses an array-factor model with statistically representative ERD fields; it is a descriptor-level interface interoperability study, not a full-wave-validated electromagnetic study or hardware prototype validation. Populating these fields from full-wave solves or measurements is identified as the natural next step for an implementation-focused follow-on. The following assumptions apply:

- Array-factor model with element-pattern roll-off omitted
- Frequency-dispersion and coupling models are phenomenological surrogates for measured unit-cell data
- Mutual coupling matrix truncated to nearest neighbors only (E- and H-plane coupling assumed identical)
- EVM metric is a phase-error-driven proxy, not a modulated-waveform link simulation
- ERD fields are statistically representative values; a production ERD would populate from HFSS/CST solves and GS RIS 008 black-box measurements

These simplifications do not affect the structural conclusion: **a single aperture synthesis survives a change of hardware class through the ERD without re-derivation.**

---

## ETSI ISG RIS Traceability Map

The ERD and SVR are designed to feed into — not replace — the ETSI ISG RIS framework. The table below maps ERD fields to ETSI functional areas.

| ETSI Functional Area | Representative ERD Fields | Phase API Role |
|---|---|---|
| Modeling (GR RIS 003) | Realized Phase Range, Amplitude Variation, Wideband Squint | Describes achievable electromagnetic behavior |
| Implementation (GR RIS 004) | Phase Quantization, Nearest-Neighbor Coupling | Describes hardware realization constraints |
| Near-Field Behavior (GR RIS 007) | Amplitude–Phase Coupling, Nearest-Neighbor Coupling | Captures local interaction effects and correction requirements |
| Testing / Verification (GS RIS 008) | Calibration Uncertainty, SVR Angular Limits | Supports validation, certification, and deployment readiness |

---

## CSI and Pilot Design Note

CSI and pilot design lie above the Phase API boundary. The Phase API does not prescribe an in-band pilot waveform, a RIS training sequence, or a cascaded-channel estimator; it supplies the hardware-side descriptor that such algorithms consume. In CSI terminology, the ERD acts as a declared prior or constraint on the RIS response, while the SVR defines the angular domain over which that prior is valid. Channel-estimation and pilot methods remain free to choose their own training protocol; they no longer need to treat the RIS hardware response as an undocumented ideal phase surface.

---

## Future Work and Call to the Community

As a perspective contribution, this article is intended to open work rather than close it — to pose a research agenda for the decade ahead that belongs to more than one community. The Phase API does not itself estimate a channel, predict a phase map, or orchestrate a handoff; it declares the hardware truth on which those activities depend. Building the control planes that exploit that declared prior is the work of the decade ahead. Natural next steps include:

- **Full-wave / measured ERD population (antenna engineers)** — Populate ERD fields (frequency grid, per-state insertion loss, coupling, SVR limits) from HFSS/CST unit-cell solves and GS RIS 008 black-box measurements for one or more real hardware classes; characterize near-field behavior and generalize the descriptor to transmitting and refracting surfaces.
- **Signal-processing integration (communications researchers)** — Incorporate ERD-declared priors and SVR validity constraints into beamforming codebooks, cascaded-channel estimators, and pilot-design frameworks so hardware behavior is exploited rather than rediscovered at runtime.
- **Network-scale SVR handoff (network researchers)** — Evaluate predictive panel handoff at the marginal SVR boundary across multi-panel deployments.
- **Community ERD profiling** — Grow an open library of populated ERDs across hardware classes, frequency bands, array geometries, and coupling models via the companion repository.

None of these require the network's permission to begin; all of them begin on the antenna engineer's bench. Contributions in any of these directions are welcome through the repository (see **Contributing**, below).

---

## Citation

### IEEE Format

R. D. Javor, "Electromagnetic Response Descriptors, Spatial Validity Regions, and the Phase API: An Antenna-Domain Interface for Reconfigurable Intelligent Surfaces in 6G," ZeroPilot Corporation, 2026.

### BibTeX

```bibtex
@article{javor2026phaseapi,
  author      = {Javor, R. D.},
  title       = {Electromagnetic Response Descriptors, {Spatial Validity Regions},
                 and the {Phase API}: {An} Antenna-Domain Interface for
                 Reconfigurable Intelligent Surfaces in {6G}},
  institution = {ZeroPilot Corporation},
  year        = {2026},
  keywords    = {RIS, reflectarray, Phase API, ERD, SVR, 6G, ETSI, GS-RIS-008,
                 aperture synthesis, unit cell, beamforming}
}
```

---

## Contributing

This repository is an open community profiling artifact. Contributions are welcome in the following areas:

- **ERD submissions** — Submit a populated ERD JSON for a hardware class not yet represented (see `schema/erd_pin_28ghz.json` as a template)
- **Traceability extensions** — Propose additions or refinements to the GS RIS 008 traceability table via pull request
- **Experiment extensions** — Additional hardware classes, array geometries, frequency bands, or coupling models
- **Schema evolution** — Proposed new ERD fields with rationale and ETSI traceability mapping

Please see `CONTRIBUTING.md` for submission guidelines and ERD field naming conventions.

---

## License

A split license model applies. The ERD JSON schema, field names, documentation text, and populated example descriptors are released under **CC0-1.0** to support royalty-free community adoption. Reference validation/parsing code is released under the **MIT License**. This dedication applies only to the schema, field names, examples, and non-normative reference code; it does not dedicate any physical RIS implementation, unit-cell design, controller architecture, calibration apparatus, or manufacturing method. See `LICENSE` for details.

---

## Acknowledgements

The reflectarray lineage underpinning this work traces to the early 1990s. Key foundational references are cited in the paper (Javor, Wu & Chang 1995; Pozar & Metzler 1993; Huang & Encinar 2007; Hum & Perruisseau-Carrier 2014). ETSI ISG RIS reference documents GR RIS 003, GR RIS 004, GR RIS 007, and GS RIS 008 provide the standards context into which the Phase API specification is designed to integrate.


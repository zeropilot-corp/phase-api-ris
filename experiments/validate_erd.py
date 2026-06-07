{
  "erd_version": "1.0",
  "hardware_class": "varactor-continuous",
  "vendor": "ExampleVendor",
  "part_number": "VAR-cont-28G-REF",
  "realized_phase_range": [
    0.0,
    360.0
  ],
  "phase_quantization_resolution": 0.0,
  "amplitude_variation_dB": 0.3,
  "amplitude_phase_coupling_dB_per_rad": 0.25,
  "nearest_neighbor_coupling_dB": -20.0,
  "operating_frequency_grid_GHz": [
    26.5,
    27.0,
    27.5,
    28.0,
    28.5,
    29.0,
    29.5
  ],
  "per_state_insertion_loss_dB": [
    -0.7
  ],
  "phase_error_rms_deg": 5.0,
  "amplitude_error_rms_dB": 0.3,
  "polarization": "linear-x",
  "calibration_uncertainty_budget_deg": 4.0,
  "temperature_drift_deg_per_C": 0.08,
  "state_transition_timing_us": 0.5,
  "svr_core_angular_limits": {
    "theta_incident_max_deg": 50.0,
    "theta_scattered_max_deg": 50.0
  },
  "svr_marginal_angular_limits": {
    "theta_incident_max_deg": 65.0,
    "theta_scattered_max_deg": 65.0
  },
  "wideband_squint_deg_per_GHz": -1.17,
  "notes": "Statistically representative varactor-tuned continuous descriptor for the Phase API hardware-swap demonstration (10x10 aperture, 28 GHz, 0.5-lambda pitch). Continuous phase control with declared amplitude-phase coupling. Values are illustrative per the perspective/tutorial scope; a production ERD would populate from full-wave solves and GS RIS 008 measurements."
}

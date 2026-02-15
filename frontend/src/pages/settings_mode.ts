export const SETTINGS_MODE = {
  Plot: {
    description: "Produces one concise figure for the current EEG selection.",
    actions: {
      "Sensor Layout": "sensor_layout",
      "Time Domain Plot": "time_domain",
      "Frequency Domain": "frequency_domain",
      "Epoch Plot": "epoch",
      "Evoked Plot": "evoked",
      "Evoked Topo Plot": "evoked_topo",
      "Evoked Plot Joint": "evoked_joint",
      "Evoked per Condition": "evoked_per_condition",
      "SNR Spectrum": "snr_spectrum",
    },
  },

  "Grid Plot": {
    description:
      "Displays per-condition results in a labeled grid for side-by-side comparison.",
    actions: {
      "PSD Grid": "psd_grid",
      "SNR Grid": "snr_grid",
      "Evoked Grid": "evoked_grid",
    },
  },

  Data: {
    description: "Provides structured tables from the current selection.",
    actions: {
      "EEG Table": null,
      "Epochs Table": null,
      Metadata: null,
    },
  },

  AI: {
    description: "AI training and inference on epochs.",
    actions: {
      Models: null,
      "Build Dataset": null,
      Train: null,
      Predict: null,
    },
  },
} as const

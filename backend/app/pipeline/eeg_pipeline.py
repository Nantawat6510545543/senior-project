class EEGPipeline:
    def __init__(self, raw):
        self.raw = raw.copy()

    def select_channels(self, ch_names):
        self.raw.pick(ch_names)
        return self

    def filter(self, l_freq=None, h_freq=None):
        if l_freq or h_freq:
            self.raw.filter(l_freq, h_freq)
        return self

    def notch(self, freq):
        if freq:
            self.raw.notch_filter(freqs=[freq])
        return self

    def resample(self, fs):
        if fs:
            self.raw.resample(fs)
        return self

    def apply_cleaning(self, flatline_sec, hf_sd):
        # placeholder
        return self

    def apply_asr(self, remove_only):
        # placeholder
        return self

    def mark_bads(self, bads):
        self.raw.info["bads"] = bads
        return self

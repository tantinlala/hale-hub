class ClimateMonitor:
    def __init__(self, get_climate_data, low_to_high_threshold, high_to_low_threshold, low_is_normal=True):
        self.low_is_normal = low_is_normal

        # Assume that climate data is in its normal state at first
        if self.low_is_normal:
            self.climate_data_is_high = False
        else:
            self.climate_data_is_high = True

        self.low_to_high_threshold = low_to_high_threshold
        self.high_to_low_threshold = high_to_low_threshold
        self.get_climate_data = get_climate_data

    def is_climate_abnormal(self):
        climate_data = self.get_climate_data()
        if not self.climate_data_is_high and climate_data > self.low_to_high_threshold:
            self.climate_data_is_high = True
        elif self.climate_data_is_high and climate_data < self.high_to_low_threshold:
            self.climate_data_is_high = False

        climate_is_abnormal = False
        if self.low_is_normal:
            if self.climate_data_is_high:
                climate_is_abnormal = True
        else:
            if not self.climate_data_is_high:
                climate_is_abnormal = True

        return climate_is_abnormal

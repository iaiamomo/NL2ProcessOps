from tools.mold_is import SensorMeasure
from tools.mold_is import AnalyzeMold
from tools.mold_is import AdjustMold
from tools.mold_is import AuthorizeProduction
class ProcessControl:
    def __init__(self):
        self.temperature_standards = (100, 200)  # Example standard range
        self.pressure_standards = (50, 150)  # Example standard range
        self.fill_rate_standards = (10, 50)  # Example standard range

    def capture_and_analyze_data(self):
        temperature, pressure, fill_rate = SensorMeasure.call()
        deviation = AnalyzeMold.call(temperature=temperature, pressure=pressure, fill_rate=fill_rate)
        return deviation

    def adjust_machine_settings(self):
        AdjustMold.call()

    def authorize_production(self):
        AuthorizeProduction.call()

    def start_process(self):
        while True:
            parameters_acceptable = self.capture_and_analyze_data()
            if not parameters_acceptable:
                self.adjust_machine_settings()
            else:
                self.authorize_production()
                break

if __name__ == "__main__":
    process_control = ProcessControl()
    process_control.start_process()
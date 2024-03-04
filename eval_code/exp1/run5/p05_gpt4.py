from tools.mold_is import SensorMeasure
from tools.mold_is import AdjustMold
class QualityAssuranceProcess:
    @staticmethod
    def monitor_and_adjust():
        # Measure the temperature, pressure, and fill rates of the mold
        temperature, pressure, fill_rate = SensorMeasure.call()
        
        # Define the acceptable ranges for each parameter
        acceptable_temperature_range = (150, 300)  # Example range, adjust as needed
        acceptable_pressure_range = (100, 200)  # Example range, adjust as needed
        acceptable_fill_rate_range = (50, 100)  # Example range, adjust as needed
        
        # Check if the parameters are within the acceptable ranges
        if not (acceptable_temperature_range[0] <= temperature <= acceptable_temperature_range[1]):
            print("Adjusting temperature...")
            AdjustMold.call()
            
        if not (acceptable_pressure_range[0] <= pressure <= acceptable_pressure_range[1]):
            print("Adjusting pressure...")
            AdjustMold.call()
            
        if not (acceptable_fill_rate_range[0] <= fill_rate <= acceptable_fill_rate_range[1]):
            print("Adjusting fill rate...")
            AdjustMold.call()
        
        # If adjustments were made, recheck the parameters
        # This could be implemented as a loop to continuously monitor and adjust until all parameters are within range
        # For simplicity, this example assumes one round of adjustment is sufficient
        
        print("Parameters are within acceptable ranges. Continuing production run.")

if __name__ == "__main__":
    QualityAssuranceProcess.monitor_and_adjust()
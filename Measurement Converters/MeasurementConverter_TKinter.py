""" 
    This is a Tkinter based measurement converter that converts between different measurement units of same type.
    (eg. metre to centimetre).

    Tkinter UI allows choosing desired measurement type, source unit, target unit and source unit measurement amount.
"""


import tkinter as tk
from tkinter import ttk


""" 
    Dictionaries to define measurement unit mapping.
    Each mapping assumes one standard unit (metre, square metre, grams, sec, Pascals, degrees) 
    and defines other units based on that.

    Eg. for length, 1mm = 0.01m, 1cm = 0.1m, 1km = 1000m
"""

length_dict = {
    'millimetres': 0.001,
    'centimetres': 0.01,
    'metres': 1,
    'kilometres': 1000,
    'miles': 1609.34,
    'feet': 0.3048,
    'inches': 0.0254,
}

area_dict = {
    'square meters': 1,
    'square kilometers': 1e6,
    'hectares': 1e4,
    'acres': 4046.86,
    'square miles': 2.59e6
}

weight_dict = {
    'grams': 1,
    'kilograms': 1000,
    'pounds': 453.592,
    'ounces': 28.3495
}

time_dict = {
    'sec': 1,
    'min': 60,
    'hrs': 3600,
    'days': 86400
}

pressure_dict = {
    'Pascals': 1,
    'atm': 101325,
    'bar': 100000,
    'psi': 6894.76
}

angle_dict = {
    'degrees': 1,
    'radians': 57.2958
}


## Hardcoded String variables
LENGTH_STRING = 'Length'
AREA_STRING = 'Area'
TIME_STRING = 'Time'
WEIGHT_STRING = 'Mass/Weight'
PRESSURE_STRING = 'Pressure'
ANGLE_STRING = 'Plane Angle'
TEMPERATURE_STRING = 'Temperature'

VALUES_STRING = 'values'

## Contant values
KELVIN_CONSTANT = 273.15   ### Constant for temperature conversion to Kelvin


## Helper Functions

### General measurement conversion
def measurement_conversion_calculator(convert_measure:dict, value:float, first_unit:float, second_unit:float) -> float:
    return value * convert_measure[first_unit] / convert_measure[second_unit]

### Temperature conversion functions
def celsius_fahrenheit_conversion(temperature):
    return (temperature * 9/5) + 32
def fahrenheit_celsius_conversion(temperature):
    return (temperature - 32) * 5/9


class Measurement_Converter(tk.Tk):
    """ 
        Class to convert between different units of Length, Mass/Weight, Area, Time, Temperature, Pressure and Angle.
    """

    def __init__(self):
        super().__init__()
        self.title("Measurement Converter")
        self.geometry("400x300")

        self.conversionFunctions = {
            LENGTH_STRING : self.lengthConversion,
            TIME_STRING : self.timeConversion,
            AREA_STRING : self.areaConversion,
            WEIGHT_STRING : self.massConversion,
            PRESSURE_STRING : self.pressureConversion,
            ANGLE_STRING : self.angleConversion,
            TEMPERATURE_STRING : self.temperatureConversion,
        }

        self.type = ttk.Label(self, text="Measurement Type: ")
        self.type.grid(column=0, row=0, padx=10, pady=10)

        self.typesMeasurement = tk.StringVar()
        self.type_drop = ttk.Combobox(self, textvariable=self.typesMeasurement)
        self.type_drop[VALUES_STRING] = tuple(self.conversionFunctions.keys())
        self.type_drop.grid(column=1, row=0, padx=10, pady=10)
        self.type_drop.bind('<<ComboboxSelected>>', self.update_units)


        self.labelInput1 = ttk.Label(self, text="Input: ")
        self.labelInput1.grid(column=0, row=1, padx=10, pady=10)
        self.labelValueInput = tk.StringVar()
        self.labelEntryInput = ttk.Entry(self, textvariable=self.labelValueInput)
        self.labelEntryInput.grid(column=1, row=1, padx=10, pady=10)


        self.conversionUnitLabel = ttk.Label(self, text="From Unit: ")
        self.conversionUnitLabel.grid(column=0, row=2, padx=10, pady=10)
        self.fromUnit = tk.StringVar()
        self.fromUnit_drop = ttk.Combobox(self, textvariable=self.fromUnit)
        self.fromUnit_drop.grid(column=1, row=2, padx=10, pady=10)


        self.conversionUnitLabel = ttk.Label(self, text="To Unit: ")
        self.conversionUnitLabel.grid(column=0, row=3, padx=10, pady=10)
        self.toUnit = tk.StringVar()
        self.toUnit_drop = ttk.Combobox(self, textvariable=self.toUnit)
        self.toUnit_drop.grid(column=1, row=3, padx=10, pady=10)


        self.buttonConvert = ttk.Button(self, text="Convert", command=self.convert)
        self.buttonConvert.grid(column=0, row=4, padx=10, pady=10)


        self.labelResult = ttk.Label(self, text="Result:")
        self.labelResult.grid(column=0, row=5, padx=10, pady=10)
        self.answerResult = ttk.Label(self, text="")
        self.answerResult.grid(column=1, row=5, padx=10, pady=10)

    
    def update_units(self, *events):
        """
            Updates the dropdown for measurement units according to measurement type selected.
        """
        
        typesMeasurement = self.typesMeasurement.get()
        units = tuple()
        if typesMeasurement == LENGTH_STRING:
            units = tuple(length_dict.keys())
        elif typesMeasurement == TIME_STRING:
            units = tuple(time_dict.keys())
        elif typesMeasurement == AREA_STRING:
            units = tuple(area_dict.keys())
        elif typesMeasurement == WEIGHT_STRING:
            units = tuple(weight_dict.keys())
        elif typesMeasurement == TEMPERATURE_STRING:
            units = ('°C', '°F', 'K')
        elif typesMeasurement == ANGLE_STRING:
            units = tuple(angle_dict.keys())
        elif typesMeasurement == PRESSURE_STRING:
            units = tuple(pressure_dict.keys())


        self.fromUnit_drop[VALUES_STRING] = units
        self.toUnit_drop[VALUES_STRING] = units


    def convert(self):
        typesMeasurement = self.typesMeasurement.get()
        input_value = float(self.labelValueInput.get())
        first_unit = self.fromUnit.get()
        second_unit = self.toUnit.get()


        if typesMeasurement in self.conversionFunctions:
            result = self.conversionFunctions[typesMeasurement](input_value, first_unit, second_unit)
            self.answerResult.config(text=f"{result} {second_unit}")

    
    def lengthConversion(self, value, first_unit, second_unit):
        convert_measure = length_dict
        return measurement_conversion_calculator(convert_measure, value, first_unit, second_unit)


    def timeConversion(self, value, first_unit, second_unit):
        convert_measure = time_dict
        return measurement_conversion_calculator(convert_measure, value, first_unit, second_unit)


    def areaConversion(self, value, first_unit, second_unit):
        convert_measure = area_dict
        return measurement_conversion_calculator(convert_measure, value, first_unit, second_unit)


    def massConversion(self, value, first_unit, second_unit):
        convert_measure = weight_dict
        return measurement_conversion_calculator(convert_measure, value, first_unit, second_unit)

    def angleConversion(self, value, first_unit, second_unit):
        convert_measure = angle_dict
        return measurement_conversion_calculator(convert_measure, value, first_unit, second_unit)


    def pressureConversion(self, value, first_unit, second_unit):
        convert_measure = pressure_dict
        return measurement_conversion_calculator(convert_measure, value, first_unit, second_unit)

    
    def temperatureConversion(self, value, first_unit, second_unit):
        if first_unit == '°C':
            if second_unit == '°F':
                return celsius_fahrenheit_conversion(value)
            elif second_unit == 'K':
                return value + KELVIN_CONSTANT
        elif first_unit == '°F':
            if second_unit == '°C':
                return fahrenheit_celsius_conversion(value)
            elif second_unit == 'K':
                return fahrenheit_celsius_conversion(value) + KELVIN_CONSTANT
        elif first_unit == 'K':
            if second_unit == '°C':
                return value - KELVIN_CONSTANT 
            elif second_unit == '°F':
                return celsius_fahrenheit_conversion(value - KELVIN_CONSTANT)
                

if __name__ == "__main__":
    app = Measurement_Converter()
    app.mainloop()

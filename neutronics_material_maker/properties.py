#!/usr/bin/env python3

"""Defines a callable property for a material."""

__author__ = "neutronics material maker development team"

import asteval
from CoolProp.CoolProp import PropsSI


class MaterialProperty:
    """
    Defines a property of a material that can be called with arguments.

    Intrinsic properties of materials, such as the density, can vary according
    to external factors, such as temperature and pressure. The MaterialProperty
    class represents this behaviour by encapsulating the details of that
    property in a way that can be called at specific values or temperature and
    pressure.

    Args:
        value (float, int, or str): This is the value of the property. It can
            be either a floating point number, in which case the property is
            constant at any temperature or press, or can be a string defining
            an equation to be evaluated at a given value of temperature_in_C,
            temperature_in_K, and/or pressure_in_Pa.
    """

    # Set any custom symbols for use in asteval
    _asteval_user_symbols = {"PropsSI": PropsSI}

    def __init__(self, value):
        self.value = value

    def __call__(
        self,
        temperature_in_C=None,
        temperature_in_K=None,
        pressure_in_Pa=None
    ):
        """
        Evaluate the property at a given temperature and/or pressure.

        Args:
            temperature_in_C (float): The temperature [°C].
            temperature_in_K (float): The temperature [K].
            pressure_in_Pa (float): The pressure [Pa].

        Returns:
            prop_val (float): The property evaluated at the given temperature
                and/or pressure.
        """
        if isinstance(self.value, str):
            aeval = asteval.Interpreter(usersyms=self._asteval_user_symbols)

            if temperature_in_C is None and temperature_in_K is not None:
                temperature_in_C = temperature_in_K - 273.15

            if temperature_in_K is None and temperature_in_C is not None:
                temperature_in_K = temperature_in_C + 273.15

            property_map = {
                "temperature_in_K": temperature_in_K,
                "temperature_in_C": temperature_in_C,
                "pressure_in_Pa": pressure_in_Pa,
            }

            # Potentially used in the eval part
            missing_values = []
            for prop_name, prop_value in property_map.items():
                aeval.symtable[prop_name] = prop_value
                if prop_name in self.value and prop_value is None:
                    missing_values.append(prop_name)

            if missing_values:
                raise ValueError("MaterialProperty requires "
                                 f"{' and '.join(missing_values)}"
                                 " to evaluate.")

            prop_val = aeval.eval(self.value)

            if len(aeval.error) > 0:
                raise aeval.error[0].exc(aeval.error[0].msg)

            return prop_val
        else:
            return self.value

    @property
    def value(self):
        """
        Get the value of the material property.

        Returns:
            value (str, float, or int): The value of the material property
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Set the value of the material property.

        Args:
            value (str, float, or int): The value of the material property
        """
        if not isinstance(value, (str, float, int)):
            raise ValueError(
                "The value of a MaterialProperty must be a string defining a "
                "temperature-/pressure-dependent function or a constant real "
                "numeric value.")

        self._value = value


class Density(MaterialProperty):
    """
    Defines a MaterialProperty to be used for Density calculations.

    Checks that the density unit is valid.

    Args:
        value (float or str): This is the value of the property. It can be
            either a floating point number, in which case the property is
            constant at any temperature or press, or can be a string defining
            an equation to be evaluated at a given value of temperature_in_C,
            temperature_in_K, and/or pressure_in_Pa.
        unit (str): The unit of the property.
    """

    _valid_units = ["g/cm3", "g/cc", "kg/m3", "atom/b-cm", "atom/cm3"]

    def __init__(self, value, unit="g/cm3"):
        self.value = value
        self.unit = unit

    @property
    def unit(self):
        """
        Get the density unit.

        Returns:
            unit (str): The density unit.
        """
        return self._unit

    @unit.setter
    def unit(self, value):
        """
        Set the density unit.

        Args:
            unit (str): The density unit.
        """
        if value not in self._valid_units:
            raise ValueError(
                f"Density unit must be one of {', '.join(self._valid_units)}."
            )

        self._unit = value

#!/usr/bin/env python3

__author__ = "neutronics material maker development team"

import pytest
import unittest

import neutronics_material_maker as nmm


class TestMaterialProperty(unittest.TestCase):
    """Defines tests for the MaterialProperty class."""

    def test_define_constant_value(self):
        """A MaterialProperty defined with a constant numeric value."""
        test_value = 3
        prop = nmm.MaterialProperty(value=test_value)
        assert prop() == test_value
        assert prop(temperature_in_C=100) == test_value
        assert prop(temperature_in_K=100) == test_value
        assert prop(pressure_in_Pa=100) == test_value

    def test_define_equation_value(self):
        """A MaterialProperty defined with a string equation value."""
        test_value = "3.75 * temperature_in_K"
        prop = nmm.MaterialProperty(value=test_value)
        with pytest.raises(ValueError):
            prop() == test_value

        calculated_value = 3.75 * 100
        assert prop(temperature_in_K=100) == pytest.approx(calculated_value)

        calculated_value = 3.75 * (100 + 273.15)
        assert prop(temperature_in_C=100) == pytest.approx(calculated_value)
        with pytest.raises(ValueError):
            prop(pressure_in_Pa=100)

    def test_validate_value(self):
        """A MaterialProperty value must be str, int, or float."""
        test_value = [1, 2, 3]
        with pytest.raises(ValueError):
            nmm.MaterialProperty(value=test_value)


class TestDensity(unittest.TestCase):
    """Defines tests for the Density class."""

    def test_validate_units(self):
        """Density units must be in the valid list."""
        for unit in nmm.Density._valid_units:
            prop = nmm.Density(value=3, unit=unit)
            assert prop is not None

        with pytest.raises(ValueError):
            nmm.Density(value=3, unit="NotAUnit")


if __name__ == "__main__":

    unittest.main()

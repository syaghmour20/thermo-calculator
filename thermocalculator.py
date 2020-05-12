from sqlconnector import Connector
from dataloader import DataLoader
from scipy.integrate import quad
import numpy as np
import sympy as sym

class ThermoCalculator:
    """This class contains various methods used to calculate thermodynamic properties."""

    def calc_enthalpy_ideal(species, t1, t2):
        """This method calculates the specific enthalpy of a species."""
        
        # Load heat capacity values for the species from the database
        constants = DataLoader.load_heat_capacity_data(species)

        if constants is None:
            print("No heat capacity data for " + species)
            return None

        a = constants[0]
        b = constants[1]
        c = constants[2]
        d = constants[3]

        # Assign a symbolic variable and create a function
        Cp = lambda x : a + b*x + c*(x**2) + d*(x**(-2))

        # Integrate function to calculate enthalpy
        enthalpy = quad(Cp, t1, t2)
        return enthalpy[0]


    def calc_entropy_ideal(species, t1, t2, p1=1, p2=1):
        """This method calculates the ideal specific entropy of a species."""
        
        # Load heat capacity values for the species from the database
        constants = DataLoader.load_heat_capacity_data(species)
        
        if constants is None:
            print("No heat capacity data for " + species)
            return None

        a = constants[0]
        b = constants[1]
        c = constants[2]
        d = constants[3]

        # Assisgn a symbolic variable and create a function
        Cp = lambda x : (a + b*x + c*(x**2) + d*(x**(-2)))/x

        # Integrate function to calculate enthalpy
        R = 8.3145
        entropy = quad(Cp, t1, t2)
        entropy = entropy[0] + R*np.log(p2/p1)
        return entropy


    def calc_enthalpy_residual(species, temp, pressure):
        """Calculates the residual enthalpy of a species at a specific temperature."""

        # Load pure species property constants for the species from the database
        constants = DataLoader.load_pure_property_data(species)

        if constants is None: 
            print("No pure property data for " + species)
            return None
        
        w = constants[1]
        tc = constants[2]
        pc = constants[3]
        R = 8.3145

        # Beginning calculations for residual properties
        t = sym.Symbol('t')
        tr = temp / tc
        pr = pressure / pc
        b0, b1, b0d, b1d = ThermoCalculator.get_virial_equations()
        
        # Final calculation for residual value
        hr = R*tc*pr*(b0.evalf(subs={t:tr}) - tr*b0d.evalf(subs={t:tr}) +
                w*(b1.evalf(subs={t:tr}) - tr*b1d.evalf(subs={t:tr})))
        
        return hr


    def calc_entropy_residual(species, temp, pressure):
        """Calculates the residual entropy of a species at a specific temperature."""
        
        # Load pure species property constants for species given
        constants = DataLoader.load_pure_property_data(species)
        
        if constants is None:
            print("No pure property data for " + species)
            return None

        w = constants[1]
        tc = constants[2]
        pc =constants[3]
        R = 8.3145

        # Begin calculations for residual properties
        t = sym.Symbol('t')
        tr = temp / tc
        pr = pressure / pc
        b0, b1, b0d, b1d = ThermoCalculator.get_virial_equations()

        # Final calculation for residual value
        sr = -R*pr*(b0d.evalf(subs={t:tr}) + w*b1d.evalf(subs={t:tr}))

        return sr


    def calc_enthalpy_real(species, t1, t2, p1, p2):
        """Calculates the real enthalpy of a species from condition one to condition two."""
        
        # Utilize the equation dH = dHig + Hr2 - Hr1
        dHig = ThermoCalculator.calc_enthalpy_ideal(species, t1, t2)
        Hr1 = ThermoCalculator.calc_enthalpy_residual(species, t1, p1)
        Hr2 = ThermoCalculator.calc_enthalpy_residual(species, t2, p2)
        
        if dHig is None or Hr1 is None or Hr2 is None:
            print("Error: unable to calculate enthalpy of the given species.")
            return None

        return dHig + Hr2 - Hr1


    def calc_entropy_real(species, t1, t2, p1, p2):
        """Calculates the real entropy of a species from condition one to condition two."""

        # Utilize the equation dS = dSig + Sr2 - Sr1
        dSig = ThermoCalculator.calc_entropy_ideal(species, t1, t2, p1, p2)
        Sr1 = ThermoCalculator.calc_entropy_residual(species, t1, p1)
        Sr2 = ThermoCalculator.calc_entropy_residual(species, t2, p2)
        
        if dSig is None or Sr1 is None or Sr2 is None:
            print("Error: unable to calculate entropy of the given species.")
            return None

        return dSig + Sr2 - Sr1

    
    def get_virial_equations():
        """Returns the equations necessary for the generalized second virial-coefficient correlation."""
        
        t = sym.Symbol('t')
        
        b0 = 0.083 - 0.442/(t**1.6)
        b1 = 0.139 - 0.172/(t**4.2)
        b0d = sym.diff(b0, t)
        b1d = sym.diff(b1, t)
        return b0, b1, b0d, b1d




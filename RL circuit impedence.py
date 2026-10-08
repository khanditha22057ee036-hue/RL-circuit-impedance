"""
RL Circuit Impedance Calculator
-------------------------------
A menu-driven program for engineering students to analyse series and
parallel RL circuits connected to an AC supply.

Key relations:
    Inductive reactance    XL = 2 * pi * f * L                (ohm)

Series RL circuit:
    Impedance              Z = R + jXL,  |Z| = sqrt(R^2 + XL^2)
    Phase angle            phi = arctan(XL / R)               (current lags voltage)
    Current                I = V / |Z|
    Voltage drops          VR = I * R,  VL = I * XL,  V = sqrt(VR^2 + VL^2)
    Power factor           cos(phi) = R / |Z|

Parallel RL circuit:
    Impedance              |Z| = (R * XL) / sqrt(R^2 + XL^2)
    Branch currents        IR = V / R,  IL = V / XL,  I = sqrt(IR^2 + IL^2)
    Phase angle            phi = arctan(R / XL)               (current lags voltage)

Other:
    Time constant          tau = L / R                        (seconds)
    Cut-off frequency      fc = R / (2 * pi * L)              (Hz)
"""

import cmath
import math


# ---------------------------------------------------------------- input helpers
def get_positive_float(prompt):
    """Keep asking until the user enters a valid positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  Please enter a value greater than zero.")
                continue
            return value
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_inductance():
    """Ask for inductance in millihenry and return it in henry."""
    return get_positive_float("Inductance L (mH): ") / 1000


# ------------------------------------------------------------------ core maths
def inductive_reactance(f, l):
    """XL = 2 * pi * f * L"""
    return 2 * math.pi * f * l


def series_impedance(r, xl):
    """Series RL: Z = R + jXL (complex number)."""
    return complex(r, xl)


def parallel_impedance(r, xl):
    """Parallel RL: Z = (R * jXL) / (R + jXL) (complex number)."""
    return (r * 1j * xl) / (r + 1j * xl)


def time_constant(r, l):
    """tau = L / R"""
    return l / r


def cutoff_frequency(r, l):
    """fc = R / (2 * pi * L)"""
    return r / (2 * math.pi * l)


# ------------------------------------------------------------------- display
def show_impedance(z):
    """Print impedance in rectangular and polar form."""
    magnitude, angle = cmath.polar(z)
    print(f"  Impedance (rectangular) Z = {z.real:.3f} + j{z.imag:.3f} ohm")
    print(f"  Impedance (polar)       Z = {magnitude:.3f} < {math.degrees(angle):.2f} deg ohm")
    print(f"  Power factor            = {math.cos(angle):.4f} lagging")


def series_rl():
    r = get_positive_float("Resistance R (ohm): ")
    l = get_inductance()
    f = get_positive_float("Frequency f (Hz): ")
    v = get_positive_float("Supply voltage V (V, rms): ")

    xl = inductive_reactance(f, l)
    z = series_impedance(r, xl)
    z_mag = abs(z)
    i = v / z_mag
    vr, vl = i * r, i * xl
    p = i ** 2 * r
    s = v * i
    q = i ** 2 * xl

    print("\n  ----- Series RL Results -----")
    print(f"  Inductive reactance XL = {xl:.3f} ohm")
    show_impedance(z)
    print(f"  Current I              = {i:.4f} A")
    print(f"  Voltage across R  (VR) = {vr:.3f} V")
    print(f"  Voltage across L  (VL) = {vl:.3f} V")
    print(f"  Active power P         = {p:.3f} W")
    print(f"  Reactive power Q       = {q:.3f} VAR")
    print(f"  Apparent power S       = {s:.3f} VA")


def parallel_rl():
    r = get_positive_float("Resistance R (ohm): ")
    l = get_inductance()
    f = get_positive_float("Frequency f (Hz): ")
    v = get_positive_float("Supply voltage V (V, rms): ")

    xl = inductive_reactance(f, l)
    z = parallel_impedance(r, xl)
    ir = v / r
    il = v / xl
    i_total = math.sqrt(ir ** 2 + il ** 2)

    print("\n  ----- Parallel RL Results -----")
    print(f"  Inductive reactance XL = {xl:.3f} ohm")
    show_impedance(z)
    print(f"  Resistor current  IR   = {ir:.4f} A")
    print(f"  Inductor current  IL   = {il:.4f} A")
    print(f"  Total current     I    = {i_total:.4f} A")


def frequency_sweep():
    r = get_positive_float("Resistance R (ohm): ")
    l = get_inductance()
    f_start = get_positive_float("Start frequency (Hz): ")
    f_stop = get_positive_float("Stop frequency (Hz): ")
    if f_stop <= f_start:
        print("  Stop frequency must be greater than start frequency.")
        return

    print(f"\n  {'f (Hz)':>10}{'XL (ohm)':>12}{'|Z| (ohm)':>12}{'Angle (deg)':>14}")
    steps = 6
    for k in range(steps):
        f = f_start + (f_stop - f_start) * k / (steps - 1)
        xl = inductive_reactance(f, l)
        z = series_impedance(r, xl)
        print(f"  {f:>10.2f}{xl:>12.3f}{abs(z):>12.3f}{math.degrees(cmath.phase(z)):>14.2f}")


def time_constant_menu():
    r = get_positive_float("Resistance R (ohm): ")
    l = get_inductance()
    tau = time_constant(r, l)
    print("\n  ----- Results -----")
    print(f"  Time constant tau   = {tau * 1000:.4f} ms")
    print(f"  Cut-off frequency   = {cutoff_frequency(r, l):.2f} Hz")
    print(f"  Current reaches 63.2% of final value in {tau * 1000:.4f} ms")
    print(f"  Current is practically steady after 5 tau = {5 * tau * 1000:.4f} ms")


def menu():
    print("\n" + "=" * 52)
    print("        RL CIRCUIT IMPEDANCE CALCULATOR")
    print("=" * 52)
    print(" 1. Series RL circuit")
    print(" 2. Parallel RL circuit")
    print(" 3. Impedance vs frequency table (series RL)")
    print(" 4. Time constant and cut-off frequency")
    print(" 0. Exit")
    print("-" * 52)


def main():
    while True:
        menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            series_rl()
        elif choice == "2":
            parallel_rl()
        elif choice == "3":
            frequency_sweep()
        elif choice == "4":
            time_constant_menu()
        elif choice == "0":
            print("\nThank you for using the calculator. Goodbye!")
            break
        else:
            print("  Invalid choice. Please select from the menu.")


if __name__ == "__main__":
    main()

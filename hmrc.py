import datetime

def get_current_tax_year():
    today = datetime.date.today()
    if today.month >= 4:
        return today.year
    else:
        return today.year - 1

def calculate_company_car_tax():
    co2_source = "CO2 emissions table source: Fleet News - https://www.fleetnews.co.uk/fleet-faq/what-are-the-current-bik-bands-/3/"
    fuel_source = "Fuel multiplier source: Fleet News - https://www.fleetnews.co.uk/fleet-faq/how-do-i-calculate-fuel-benefit-tax"
    
    print(co2_source)
    print(fuel_source)
    
    current_tax_year = get_current_tax_year()
    print(f"Calculating company car tax for the tax year: {current_tax_year}/{current_tax_year + 1}")

    try:
        car_make_model = input("Enter the car make and model: ")
        co2_emissions = int(input("Enter the CO2 emissions (in g/km): "))
        p11d_value = float(input("Enter the P11D value of the car: "))
        tax_rate = int(input("Enter your personal income tax rate (20, 40, or 45): "))
        duration = input("Enter the duration of car use (e.g., whole tax year): ")

        is_phev = input("Is the car a plug-in hybrid electric vehicle (PHEV)? (yes/no): ").strip().lower() == 'yes'
        electric_range = 0
        if is_phev:
            electric_range = int(input("Enter the electric-only range in miles: "))

        bik_rate = determine_bik_rate(co2_emissions, electric_range, is_phev)
        print(f"Determined BiK Rate: {bik_rate}% based on CO2 emissions and electric range.")

        taxable_benefit = p11d_value * (bik_rate / 100)
        print(f"Calculated Taxable Benefit: £{taxable_benefit:.2f} (P11D Value: £{p11d_value} * BiK Rate: {bik_rate}%)")

        tax_payable = taxable_benefit * (tax_rate / 100)
        print(f"Calculated Tax Payable: £{tax_payable:.2f} (Taxable Benefit: £{taxable_benefit} * Tax Rate: {tax_rate}%)")

        include_fuel = input("Do you want to include the fuel benefit? (yes/no): ").strip().lower() == 'yes'
        fuel_benefit = 0
        fuel_tax_payable = 0

        if include_fuel:
            fuel_multiplier = 27800
            fuel_benefit = calculate_fuel_benefit(fuel_multiplier, bik_rate)
            print(f"Fuel Benefit: £{fuel_benefit:.2f} (Fuel Multiplier: £{fuel_multiplier} * BiK Rate: {bik_rate}%)")

            fuel_tax_payable = fuel_benefit * (tax_rate / 100)
            print(f"Calculated Fuel Tax Payable: £{fuel_tax_payable:.2f} (Fuel Benefit: £{fuel_benefit} * Tax Rate: {tax_rate}%)")

        total_annual_tax = tax_payable + fuel_tax_payable
        total_monthly_tax = total_annual_tax / 12

        # Additional Information Section
        additional_info = """
        Additional Information:
        -----------------------
        - P11D Value: The list price of the car including VAT and any delivery charges, but excluding the first year registration fee and vehicle tax.
        - BiK Rate: The Benefit-in-Kind rate is a percentage applied to the P11D value to determine the taxable benefit.
        - CO2 Emissions: The amount of carbon dioxide emitted by the car, measured in grams per kilometer.
        - Fuel Benefit: An additional taxable benefit if the employer provides fuel for private use.
        """

        results = f"""
        Company Car Tax Calculation Results:
        ------------------------------------
        Car Make and Model: {car_make_model}
        CO2 Emissions: {co2_emissions} g/km
        P11D Value: £{p11d_value:.2f}
        Personal Tax Rate: {tax_rate}%
        BiK Rate: {bik_rate}%
        Taxable Benefit Calculation: £{p11d_value} * {bik_rate}% = £{taxable_benefit:.2f}
        Annual Company Car Tax: £{taxable_benefit} * {tax_rate}% = £{tax_payable:.2f}
        Monthly Company Car Tax: £{tax_payable / 12:.2f}
        """

        if include_fuel:
            results += f"""
        Fuel Multiplier: £{fuel_multiplier}
        Fuel Benefit Calculation: £{fuel_multiplier} * {bik_rate}% = £{fuel_benefit:.2f}
        Annual Fuel Tax Payable: £{fuel_benefit} * {tax_rate}% = £{fuel_tax_payable:.2f}
        Monthly Fuel Tax Payable: £{fuel_tax_payable / 12:.2f}
        """

        results += f"""
        Total Annual Tax Payable: £{total_annual_tax:.2f}
        Total Monthly Tax Payable: £{total_monthly_tax:.2f}
        """

        # Combine results and additional information
        full_message = results + additional_info

        print(full_message)

        with open("company_car_tax_results.txt", "w") as file:
            file.write(co2_source + "\n")
            file.write(fuel_source + "\n")
            file.write(full_message)

    except ValueError as e:
        print(f"Input error: {e}. Please enter valid numbers for CO2 emissions, P11D value, and tax rate.")

def determine_bik_rate(co2_emissions, electric_range, is_phev):
    bik_rates = [
        (0, 0, None, 2),
        (1, 50, 130, 2),
        (1, 50, 70, 5),
        (1, 50, 40, 8),
        (1, 50, 30, 12),
        (1, 50, 0, 14),
        (51, 54, None, 15),
        (55, 59, None, 16),
        (60, 64, None, 17),
        (65, 69, None, 18),
        (70, 74, None, 19),
        (75, 79, None, 20),
        (80, 84, None, 21),
        (85, 89, None, 22),
        (90, 94, None, 23),
        (95, 99, None, 24),
        (100, 104, None, 25),
        (105, 109, None, 26),
        (110, 114, None, 27),
        (115, 119, None, 28),
        (120, 124, None, 29),
        (125, 129, None, 30),
        (130, 134, None, 31),
        (135, 139, None, 32),
        (140, 144, None, 33),
        (145, 149, None, 34),
        (150, 154, None, 35),
        (155, 159, None, 36),
        (160, 169, None, 37),
        (170, float('inf'), None, 37)
    ]

    for min_co2, max_co2, min_range, rate in bik_rates:
        if min_co2 <= co2_emissions <= max_co2:
            if min_range is None or electric_range >= min_range:
                return rate

    return 37

def calculate_fuel_benefit(fuel_multiplier, bik_rate):
    return fuel_multiplier * (bik_rate / 100)

calculate_company_car_tax()

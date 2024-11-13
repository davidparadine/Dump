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
        p11d_value = float(input("Enter the P11D value of the car: "))
        tax_rate = int(input("Enter your personal income tax rate (20, 40, or 45): "))
        
        # Input for the date when the car was received in UK format
        car_received_date_str = input("Enter the date when you received the car (DD/MM/YYYY) or leave blank for full year use: ").strip()
        
        if car_received_date_str:
            car_received_date = datetime.datetime.strptime(car_received_date_str, "%d/%m/%Y").date()
            # Calculate the number of days the car is used in the tax year
            tax_year_end_date = datetime.date(current_tax_year + 1, 4, 5)
            days_used = (tax_year_end_date - car_received_date).days
        else:
            # Assume full year use
            days_used = 365
            # Initialize car_received_date to the start of the tax year
            car_received_date = datetime.date(current_tax_year, 4, 6)
            # Initialize tax_year_end_date for full year use
            tax_year_end_date = datetime.date(current_tax_year + 1, 4, 5)

        print(f"Days the car is used: {days_used}")

        # Ask if the car is purely electric
        is_pure_electric = input("Is the car purely electric? (yes/no): ").strip().lower() == 'yes'

        # If the car is not purely electric, ask for CO2 emissions
        co2_emissions = 0
        if not is_pure_electric:
            co2_emissions = int(input("Enter the CO2 emissions (in g/km): "))

        # Ask if the car is a plug-in hybrid electric vehicle (PHEV)
        is_phev = False
        electric_range = 0
        if not is_pure_electric:
            is_phev = input("Is the car a plug-in hybrid electric vehicle (PHEV)? (yes/no): ").strip().lower() == 'yes'
            if is_phev:
                electric_range = int(input("Enter the electric-only range in miles: "))

        bik_rate = determine_bik_rate(co2_emissions, electric_range, is_phev)
        print(f"Determined BiK Rate: {bik_rate}% based on CO2 emissions and electric range.")

        # Step 1: Calculate the full-year tax amount
        taxable_benefit = p11d_value * (bik_rate / 100)
        print(f"Calculated Taxable Benefit: £{taxable_benefit:.2f} (P11D Value: £{p11d_value} * BiK Rate: {bik_rate}%)")

        full_year_tax = taxable_benefit * (tax_rate / 100)
        print(f"Calculated Full-Year Tax: £{full_year_tax:.2f} (Taxable Benefit: £{taxable_benefit} * Tax Rate: {tax_rate}%)")

        # Step 2: Determine the proportion of the tax year
        total_days_in_tax_year = 365
        proportion_of_year = days_used / total_days_in_tax_year
        print(f"Proportion of the year the car is used: {proportion_of_year:.4f}")

        # Step 3: Calculate the pro-rata tax amount
        pro_rata_tax = full_year_tax * proportion_of_year
        print(f"Pro-Rata Tax (from {car_received_date.strftime('%d/%m/%Y')} to {tax_year_end_date.strftime('%d/%m/%Y')}): £{pro_rata_tax:.2f}")

        include_fuel = False
        fuel_benefit = 0
        fuel_tax = 0

        if not is_pure_electric:
            include_fuel = input("Do you want to include the fuel benefit? (yes/no): ").strip().lower() == 'yes'
            if include_fuel:
                fuel_multiplier = get_fuel_multiplier()
                fuel_benefit = calculate_fuel_benefit(fuel_multiplier, bik_rate)
                print(f"Fuel Benefit: £{fuel_benefit:.2f} (Fuel Multiplier: £{fuel_multiplier} * BiK Rate: {bik_rate}%)")

                # Calculate full-year fuel tax
                full_year_fuel_tax = fuel_benefit * (tax_rate / 100)
                print(f"Full-Year Fuel Tax: £{full_year_fuel_tax:.2f}")

                # Calculate pro-rata fuel tax
                fuel_tax = full_year_fuel_tax * proportion_of_year
                print(f"Pro-Rata Fuel Tax (from {car_received_date.strftime('%d/%m/%Y')} to {tax_year_end_date.strftime('%d/%m/%Y')}): £{fuel_tax:.2f}")

        # Ask if the user has a company van
        has_company_van = input("Do you have a company van? (yes/no): ").strip().lower() == 'yes'
        van_tax = 0
        van_fuel_tax = 0

        if has_company_van:
            is_zero_emission = input("Is the van zero-emission? (yes/no): ").strip().lower() == 'yes'
            van_tax, van_fuel_tax = calculate_van_tax(tax_rate, include_fuel, is_zero_emission)
            print(f"Company Van Tax: £{van_tax:.2f}")
            if include_fuel:
                print(f"Company Van Fuel Tax: £{van_fuel_tax:.2f}")

        total_annual_tax = pro_rata_tax + fuel_tax + van_tax + (van_fuel_tax if has_company_van and include_fuel else 0)

        # Simplified summary
        summary = f"""
        ================================
        Company Car and Van Tax Summary for {current_tax_year}/{current_tax_year + 1}
        ================================
        Total Full-Year Tax: £{full_year_tax + (full_year_fuel_tax if include_fuel else 0) + van_tax + (van_fuel_tax if include_fuel else 0):.2f}
        Total Pro-Rata Tax: £{total_annual_tax:.2f}
        """

        # Detailed calculations
        details = f"""
        ==========================================
        Detailed Company Car and Van Tax Calculation
        ==========================================

        Car Details:
        ------------
        - Make and Model: {car_make_model}
        - CO2 Emissions: {co2_emissions} g/km
        - P11D Value: £{p11d_value:.2f}

        Car Tax Details:
        ----------------
        - Personal Tax Rate: {tax_rate}%
        - BiK Rate: {bik_rate}%
        - Taxable Benefit Calculation: £{p11d_value} * {bik_rate}% = £{taxable_benefit:.2f}
        - Full-Year Car Tax: £{full_year_tax:.2f}
        - Pro-Rata Car Tax (from {car_received_date.strftime('%d/%m/%Y')} to {tax_year_end_date.strftime('%d/%m/%Y')}): £{pro_rata_tax:.2f}
        """

        if include_fuel:
            details += f"""
        Car Fuel Benefit (if applicable):
        ---------------------------------
        - Fuel Multiplier: £{fuel_multiplier}
        - Fuel Benefit Calculation: £{fuel_multiplier} * {bik_rate}% = £{fuel_benefit:.2f}
        - Full-Year Car Fuel Tax: £{full_year_fuel_tax:.2f}
        - Pro-Rata Car Fuel Tax (from {car_received_date.strftime('%d/%m/%Y')} to {tax_year_end_date.strftime('%d/%m/%Y')}): £{fuel_tax:.2f}
        """

        if has_company_van:
            details += f"""
        Van Tax (if applicable):
        ------------------------
        - Van Benefit Charge: £{3960 if not is_zero_emission else 0}
        - Van Tax Calculation: £{3960 if not is_zero_emission else 0} * {tax_rate}% = £{van_tax:.2f}
        """

            if include_fuel:
                details += f"""
        Van Fuel Benefit (if applicable):
        ---------------------------------
        - Van Fuel Benefit Charge: £757
        - Van Fuel Tax Calculation: £757 * {tax_rate}% = £{van_fuel_tax:.2f}
        """

        # Calculate total full-year and pro-rata taxes
        total_full_year_car_tax = full_year_tax + (full_year_fuel_tax if include_fuel else 0)
        total_full_year_van_tax = van_tax + (van_fuel_tax if include_fuel else 0)
        total_pro_rata_car_tax = pro_rata_tax + (fuel_tax if include_fuel else 0)
        total_pro_rata_van_tax = van_tax + (van_fuel_tax if include_fuel else 0)

        details += f"""
        Total Tax Breakdown:
        --------------------
        - Total Full-Year Car Tax: £{total_full_year_car_tax:.2f}
        - Total Full-Year Van Tax: £{total_full_year_van_tax:.2f}
        - Total Pro-Rata Car Tax: £{total_pro_rata_car_tax:.2f}
        - Total Pro-Rata Van Tax: £{total_pro_rata_van_tax:.2f}

        Additional Information:
        -----------------------
        - P11D Value: The list price of the car including VAT and any delivery charges, but excluding the first year registration fee and vehicle tax.
        - BiK Rate: The Benefit-in-Kind rate is a percentage applied to the P11D value to determine the taxable benefit.
        - CO2 Emissions: The amount of carbon dioxide emitted by the car, measured in grams per kilometer.
        - Fuel Benefit: An additional taxable benefit if the employer provides fuel for private use.

        Sources:
        --------
        - {co2_source}
        - {fuel_source}
        """

        # Write to fileuestio
        with open("company_car_tax_results.txt", "w") as file:
            file.write(summary)
            file.write("\n\n")
            file.write(details)

        print(summary)
        print(details)

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

def get_fuel_multiplier():
    fuel_multipliers = {
        2023: 27800,
    }

    return fuel_multipliers.get(2023, 27800)

def calculate_fuel_benefit(fuel_multiplier, bik_rate):
    return fuel_multiplier * (bik_rate / 100)

def calculate_van_tax(tax_rate, include_fuel, is_zero_emission=False):
    # Van Benefit Charge (VBC) for 2023/24
    van_benefit_charge = 3960 if not is_zero_emission else 0

    # Calculate the van tax based on the employee's income tax rate
    van_tax = van_benefit_charge * (tax_rate / 100)

    # Van Fuel Benefit for 2023/24
    van_fuel_benefit_charge = 757 if include_fuel else 0
    van_fuel_tax = van_fuel_benefit_charge * (tax_rate / 100)

    return van_tax, van_fuel_tax

calculate_company_car_tax()

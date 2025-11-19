# ------------------------------------------------------------
# 💰 COOKIE CLICKER ECONOMIC ADVISOR SCRIPT (Menu-Driven)
# ------------------------------------------------------------
# Provides two choices:
# 1. MRPC Comparison (Which of 2+ available assets is best now?)
# 2. Intertemporal Analysis (Should I save for the next expensive building?)
# ------------------------------------------------------------

def calculate_mrpc(cost, cps_gained):
    """Calculates Marginal Return Per Cost."""
    if cost <= 0 or cps_gained <= 0:
        return 0
    return cps_gained / cost


def get_asset_details(asset_number, prompt_name="Asset"):
    """Prompts the user for cost and CPS gain for one asset."""
    print(f"\n--- {prompt_name} Details ---")
    name = input(f"Enter Name of {prompt_name} {asset_number}: ")
    try:
        cost = float(input(f"Enter Cost of {name}: "))
        cps = float(input(f"Enter CPS Gain from {name}: "))
        if cost < 0 or cps < 0:
            print("Cost and CPS must be non-negative.")
            return None, 0, 0
        return name, cost, cps
    except ValueError:
        print("Invalid input. Please enter numbers for cost and CPS.")
        return None, 0, 0


def find_best_asset(assets):
    """Finds the asset with the highest MRPC."""
    best_asset = None
    highest_mrpc = -1

    for asset in assets:
        if asset['mrpc'] > highest_mrpc:
            highest_mrpc = asset['mrpc']
            best_asset = asset

    return best_asset


# --- CHOICE 1: MRPC Comparison (2+ Buildings) ---

def run_mrpc_comparison(current_cps):
    """Handles the comparison of 2+ currently available investments."""
    assets = []

    print("\n--- Running MRPC Comparison (2+ Assets) ---")

    # Get details for assets 1 and 2 (minimum required)
    for i in range(1, 3):
        name, cost, cps = get_asset_details(i)
        if name:
            assets.append({'name': name, 'cost': cost, 'cps': cps, 'mrpc': calculate_mrpc(cost, cps)})

    # Allow comparison of more assets
    asset_count = 3
    while True:
        more = input("\nDo you want to compare another asset? (y/n): ").lower()
        if more != 'y':
            break

        name, cost, cps = get_asset_details(asset_count)
        if name:
            assets.append({'name': name, 'cost': cost, 'cps': cps, 'mrpc': calculate_mrpc(cost, cps)})
            asset_count += 1

    if not assets:
        print("\nNo assets entered for comparison.")
        return

    best_asset = find_best_asset(assets)

    # --- Display Results ---
    print("\n" + "=" * 50)
    print("📈 MRPC COMPARISON RESULTS 📈")
    print("=" * 50)
    print(f"Current CPS: {current_cps:,.2f}")
    print("-" * 50)

    for asset in assets:
        # Calculate time-to-payback for better context (Payback Time = Cost / Total_New_CPS)
        payback_time = asset['cost'] / (current_cps + asset['cps']) if (current_cps + asset['cps']) > 0 else float(
            'inf')

        print(
            f"[{asset['name']}] Cost: {asset['cost']:,.2f} | CPS Gain: {asset['cps']:,.2f} | MRPC: {asset['mrpc']:.8f} | Payback: {payback_time:,.0f}s")

    print("\n" + "-" * 50)
    if best_asset:
        print(f"🎉 **BUY THIS ASSET NOW:** {best_asset['name'].upper()}")
        print(f"   Reason: Highest Marginal Return Per Cost (MRPC: {best_asset['mrpc']:.8f})")
    else:
        print("Could not determine the best asset.")
    print("-" * 50)


# --- CHOICE 2: Intertemporal Analysis (Buy Cheap Now or Save?) ---

def run_intertemporal_analysis(current_cps):
    """Handles the 'Should I wait for the next expensive tier?' decision."""

    print("\n--- Running Intertemporal Analysis (Buy Now or Save?) ---")
    print("Comparing a small, affordable asset (A) vs. a huge, expensive asset (B).")

    # Get details for the Cheap Asset (A)
    name_a, cost_a, cps_a = get_asset_details("A", prompt_name="Cheap Asset (Buy Now)")
    if not name_a: return

    # Get details for the Expensive Asset (B)
    name_b, cost_b, cps_b = get_asset_details("B", prompt_name="Expensive Asset (Save For)")
    if not name_b: return

    if current_cps <= 0:
        print("Error: Current CPS must be greater than zero for time-based analysis.")
        return

    # Economic Calculations
    wait_time_seconds = cost_b / current_cps
    extra_earnings = cps_a * wait_time_seconds

    # --- Display Results ---
    print("\n" + "=" * 50)
    print("⏳ INTERTEMPORAL DECISION RESULTS ⏳")
    print("=" * 50)
    print(f"Time needed to save for {name_b} (without buying {name_a}): {wait_time_seconds:,.2f} seconds")
    print(f"Extra cookies earned during that wait time (if buying {name_a} now): {extra_earnings:,.2f}")
    print(f"Cost of {name_a}: {cost_a:,.2f}")
    print("-" * 50)

    if extra_earnings > cost_a:
        print(
            f"\n✅ DECISION: **BUY {name_a.upper()} NOW.** (The extra earnings of {extra_earnings:,.2f} justify the cost.)")
        print(f"   Gain/Loss: +{extra_earnings - cost_a:,.2f}")
    else:
        print(
            f"\n❌ DECISION: **SAVE FOR {name_b.upper()}.** (The extra earnings of {extra_earnings:,.2f} do NOT justify the cost.)")
        print(f"   Gain/Loss: -{cost_a - extra_earnings:,.2f}")
    print("-" * 50)


# ============================================================
# MAIN EXECUTION WITH MENU
# ============================================================

def main():
    print("\n" + "#" * 50)
    print("## 🍪 Cookie Clicker Economic Advisor ##")
    print("## Choose your optimization goal: ##")
    print("#" * 50)

    try:
        current_cps = float(input("First, enter your **CURRENT** total Cookies Per Second (CPS): "))
    except ValueError:
        print("Invalid input for Current CPS. Exiting.")
        return

    if current_cps < 0:
        print("CPS cannot be negative. Exiting.")
        return

    while True:
        print("\n" + "-" * 50)
        print("1. ⚖️ **Compare 2+ Available Buildings/Upgrades** (MRPC Analysis)")
        print("2. ⏳ **Ask When to Buy the Next Expensive Tier** (Intertemporal Analysis)")
        print("3. Exit")
        print("-" * 50)

        choice = input("Enter choice (1, 2, or 3): ")

        if choice == '1':
            run_mrpc_comparison(current_cps)
        elif choice == '2':
            run_intertemporal_analysis(current_cps)
        elif choice == '3':
            print("\nExiting Advisor. Happy clicking! 🍪")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()

from flask import Flask, render_template, request, flash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "supersecret"  # Needed for flash messages

# Nepali currency formatting
def nepali_currency(value):
    if value is None:
        return ""
    value = int(round(value))
    s = str(value)
    if len(s) <= 3:
        return s
    last_three = s[-3:]
    remaining = s[:-3]
    parts = []
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        parts.insert(0, remaining)
    return ",".join(parts) + "," + last_three

app.jinja_env.filters['nep_currency'] = nepali_currency

@app.route("/")
def home():
    return render_template("index.html")

# ================= EMI CALCULATOR =================
@app.route("/emi", methods=["GET", "POST"])
def emi():
    emi_value = total_payment = total_interest = None
    principal = rate = years = None
    errors = []

    if request.method == "POST":
        try:
            principal = request.form.get("principal")
            rate = request.form.get("rate")
            years = request.form.get("years")

            # Validate empty fields
            if not principal or not rate or not years:
                errors.append("All fields are required.")
            else:
                principal = float(principal)
                rate = float(rate)
                years = float(years)

                # Validate numeric values
                if principal <= 0:
                    errors.append("Principal must be greater than 0.")
                if rate <= 0 or rate > 100:
                    errors.append("Interest rate must be between 0 and 100%.")
                if years <= 0:
                    errors.append("Duration must be greater than 0 years.")

            # EMI calculation
            if not errors:
                N = years * 12
                monthly_rate = rate / (12 * 100)
                emi_value = round(
                    principal * monthly_rate * (1 + monthly_rate) ** N /
                    ((1 + monthly_rate) ** N - 1), 2
                )
                total_payment = round(emi_value * N, 2)
                total_interest = round(total_payment - principal, 2)

        except ValueError:
            errors.append("Please enter valid numeric values.")

        # Flash errors
        for error in errors:
            flash(error, "error")

    return render_template(
        "emi.html",
        emi=emi_value,
        total_payment=total_payment,
        total_interest=total_interest,
        principal=principal,
        rate=rate,
        years=years
    )

# ================= LOAN CALCULATOR =================
@app.route("/loan", methods=["GET", "POST"])
def loan():
    emi_value = total_payment = total_interest = None
    principal = down_payment = principal_after_down = rate = years = None
    errors = []

    if request.method == "POST":
        try:
            principal = request.form.get("principal")
            down_payment = request.form.get("down_payment", 0)
            rate = request.form.get("rate")
            years = request.form.get("years")

            # Empty field check
            if not principal or not rate or not years:
                errors.append("Principal, Interest Rate, and Duration are required.")
            else:
                principal = float(principal)
                down_payment = float(down_payment or 0)
                rate = float(rate)
                years = float(years)
                principal_after_down = principal - down_payment

                # Numeric validations
                if principal <= 0:
                    errors.append("Principal must be greater than 0.")
                if down_payment < 0 or down_payment > principal:
                    errors.append("Down payment must be between 0 and principal.")
                if rate <= 0 or rate > 100:
                    errors.append("Interest rate must be between 0 and 100%.")
                if years <= 0:
                    errors.append("Duration must be greater than 0 years.")

            # EMI calculation
            if not errors:
                N = years * 12
                monthly_rate = rate / (12 * 100)
                emi_value = round(
                    principal_after_down * monthly_rate * (1 + monthly_rate) ** N /
                    ((1 + monthly_rate) ** N - 1), 2
                )
                total_payment = round(emi_value * N, 2)
                total_interest = round(total_payment - principal_after_down, 2)

        except ValueError:
            errors.append("Please enter valid numeric values.")

        # Flash errors
        for error in errors:
            flash(error, "error")

    return render_template(
        "loan.html",
        emi=emi_value,
        total_payment=total_payment,
        total_interest=total_interest,
        principal=principal,
        down_payment=down_payment,
        principal_after_down=principal_after_down,
        rate=rate,
        years=years
    )

# ================= FUEL CALCULATOR =================
@app.route("/fuel", methods=["GET", "POST"])
def fuel():
    total_cost = distance = mileage = price = None
    errors = []

    if request.method == "POST":
        try:
            distance = request.form.get("distance")
            mileage = request.form.get("mileage")
            price = request.form.get("price")

            # Empty field check
            if not distance or not mileage or not price:
                errors.append("All fields are required.")
            else:
                distance = float(distance)
                mileage = float(mileage)
                price = float(price)

                # Numeric validations
                if distance <= 0:
                    errors.append("Distance must be greater than 0.")
                if mileage <= 0:
                    errors.append("Mileage must be greater than 0.")
                if price < 0:
                    errors.append("Fuel price cannot be negative.")

            if not errors:
                total_cost = round((distance / mileage) * price, 2)

        except ValueError:
            errors.append("Please enter valid numeric values.")

        for error in errors:
            flash(error, "error")

    return render_template(
        "fuel.html",
        total_cost=total_cost,
        distance=distance,
        mileage=mileage,
        price=price
    )

if __name__ == "__main__":
    app.run(debug=True)

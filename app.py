from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route("/emi", methods=["GET", "POST"])
def emi():
    emi_value = total_payment = total_interest = None
    principal = rate = years = None

    if request.method == "POST":
        principal = float(request.form["principal"])
        rate = float(request.form["rate"])
        years = float(request.form["years"])

        N = years * 12
        monthly_rate = rate / (12 * 100)

        emi_value = round(
            principal * monthly_rate * (1 + monthly_rate)**N /
            ((1 + monthly_rate)**N - 1), 2
        )

        total_payment = round(emi_value * N, 2)
        total_interest = round(total_payment - principal, 2)

    return render_template(
        "emi.html",
        emi=emi_value,
        total_payment=total_payment,
        total_interest=total_interest,
        principal=principal,
        rate=rate,
        years=years
    )

@app.route("/loan", methods=["GET", "POST"])
def loan():
    emi_value = total_payment = total_interest = None
    principal = down_payment = principal_after_down = rate = years = None

    if request.method == "POST":
        principal = float(request.form["principal"])
        down_payment = float(request.form.get("down_payment", 0))
        principal_after_down = principal - down_payment
        rate = float(request.form["rate"])
        years = float(request.form["years"])

        N = years * 12
        monthly_rate = rate / (12 * 100)

        emi_value = round(
            principal_after_down * monthly_rate * (1 + monthly_rate)**N /
            ((1 + monthly_rate)**N - 1), 2
        )

        total_payment = round(emi_value * N, 2)
        total_interest = round(total_payment - principal_after_down, 2)

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

@app.route("/fuel", methods=["GET", "POST"])
def fuel():
    total_cost = distance = mileage = price = None

    if request.method == "POST":
        distance = float(request.form["distance"])
        mileage = float(request.form["mileage"])
        price = float(request.form["price"])
        total_cost = round((distance / mileage) * price, 2)

    return render_template(
        "fuel.html",
        total_cost=total_cost,
        distance=distance,
        mileage=mileage,
        price=price
    )

if __name__ == "__main__":
    app.run(debug=True)

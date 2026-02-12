from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

from flask import request

@app.route("/emi", methods=["GET", "POST"])
def emi():
    emi_value = None
    total_payment = None
    total_interest = None

    if request.method == "POST":
        # Get form data
        P = float(request.form["principal"])
        R = float(request.form["rate"])
        N = float(request.form["years"]) * 12  # convert years to months
        monthly_rate = R / (12 * 100)

        # EMI formula
        emi_value = round(P * monthly_rate * (1 + monthly_rate)**N / ((1 + monthly_rate)**N - 1), 2)
        total_payment = round(emi_value * N, 2)
        total_interest = round(total_payment - P, 2)

    return render_template(
        "emi.html",
        emi=emi_value,
        total_payment=total_payment,
        total_interest=total_interest
    )
@app.route("/loan", methods=["GET", "POST"])
def loan():
    emi_value = None
    total_payment = None
    total_interest = None
    principal_after_down = None

    if request.method == "POST":
        P = float(request.form["principal"])
        down_payment = float(request.form.get("down_payment", 0))
        principal_after_down = P - down_payment
        R = float(request.form["rate"])
        N = float(request.form["years"]) * 12
        monthly_rate = R / (12 * 100)

        # EMI formula
        emi_value = round(principal_after_down * monthly_rate * (1 + monthly_rate)**N / ((1 + monthly_rate)**N - 1), 2)
        total_payment = round(emi_value * N, 2)
        total_interest = round(total_payment - principal_after_down, 2)

    return render_template(
        "loan.html",
        emi=emi_value,
        total_payment=total_payment,
        total_interest=total_interest,
        principal_after_down=principal_after_down
    )

@app.route("/fuel", methods=["GET", "POST"])
def fuel():
    total_cost = None

    if request.method == "POST":
        distance = float(request.form["distance"])
        mileage = float(request.form["mileage"])
        price = float(request.form["price"])

        # Fuel cost formula
        total_cost = round((distance / mileage) * price, 2)

    return render_template("fuel.html", total_cost=total_cost)


if __name__ == "__main__":
    app.run(debug=True)

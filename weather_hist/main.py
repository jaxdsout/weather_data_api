import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)


stations = pd.read_csv("dataset/stations.txt", skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']].squeeze()
print(stations)

@app.route("/")
def home():
    return render_template("index.html", data=stations.to_html())


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "dataset/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient='records')
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def year_data(station, year):
    filename = "dataset/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient='records')
    return result


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "dataset/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    celsius = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    fahrenheit = celsius * (9/5) + 32
    kelvin = celsius + 273.15
    return {"station": station,
            "date": date,
            "celsius": celsius,
            "fahrenheit": fahrenheit,
            "kelvin": kelvin
            }


if __name__ == "__main__":
    app.run(port=8002, debug=True)

import pandas as pd
import matplotlib.pyplot as plt

base = "https://data.wprdc.org/datastore/dump/"
properties = pd.read_csv(
    base + "0a963f26-eb4b-4325-bbbc-3ddf6a871410",
    usecols=["parcel_id", "neighborhood"],
    dtype="string"
)
city = pd.read_csv(
    base + "668d7238-cfd2-492e-b397-51a6e74182ff",
    usecols=["hood"],
    dtype="string"
)

properties["neighborhood"] = properties["neighborhood"].str.strip()
properties["parcel_id"] = properties["parcel_id"].str.strip()
properties = properties.replace("", pd.NA).dropna()
names = city["hood"].str.strip().dropna().unique()

unmatched = set(properties["neighborhood"]) - set(names)
if unmatched:
    raise ValueError(f"Check these neighborhood names: {sorted(unmatched)}")

counts = properties.groupby("neighborhood")["parcel_id"].nunique()
counts = counts.reindex(names, fill_value=0).sort_values()
ranks = counts.rank(method="average")
results = pd.DataFrame({"condemned_parcels": counts, "rank": ranks})
print(results.to_string())

counts.tail(10).plot.barh()
plt.xlabel("Unique condemned parcels")
plt.title("Pittsburgh neighborhoods with the most listed condemned parcels")
plt.tight_layout()
plt.show()

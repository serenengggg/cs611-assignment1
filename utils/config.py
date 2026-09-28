"""Central configuration: paths and label-definition parameters."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
DATAMART = os.path.join(ROOT, "datamart")
BRONZE = os.path.join(DATAMART, "bronze")
SILVER = os.path.join(DATAMART, "silver")
GOLD = os.path.join(DATAMART, "gold")

# source name -> raw csv
SOURCES = {
    "clickstream": "feature_clickstream.csv",
    "attributes": "features_attributes.csv",
    "financials": "features_financials.csv",
    "lms_loan_daily": "lms_loan_daily.csv",
}

# Label definition (same as Lab 2): default = >= LABEL_DPD days past due at LABEL_MOB months on book
LABEL_MOB = 6
LABEL_DPD = 30

import pandas as pd
import os

class TrafficData:
    def __init__(self):
        # Correct path to the dataset
        csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'traffic_counts_datasd.csv'))
        self.traffic_df = self.load_data(csv_path)

    def load_data(self, path):
        try:
            df = pd.read_csv(path)
            if 'street_name' not in df.columns:
                print(f"⚠️ 'street_name' column not found. Columns: {df.columns.tolist()}")
                return pd.DataFrame()
            df['street_name'] = df['street_name'].astype(str).str.upper()
            return df
        except Exception as e:
            print(f"⚠️ Error loading traffic CSV: {e}")
            return pd.DataFrame()

    def get_average_speed(self, street_name):
        if self.traffic_df.empty:
            return None

        street_name = street_name.upper()
        matches = self.traffic_df[self.traffic_df['street_name'].str.contains(street_name, na=False)]

        if not matches.empty:
            # No 'Average Speed' in dataset, so we could simulate or return average count
            if 'total_count' in matches.columns:
                return matches['total_count'].mean()
            else:
                print("⚠️ 'total_count' column not found in dataset.")
                return None

        return None

# Singleton instance for reuse
traffic_data_instance = TrafficData()

def get_average_speed(street_name):
    return traffic_data_instance.get_average_speed(street_name)










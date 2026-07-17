from backend.agents.data_cleaning_agent import DataCleaner

cleaner = DataCleaner()

df = cleaner.read_dataset("uploads/ecommerce_data.csv")

report = cleaner.analyze_dataset(df)

print(report)
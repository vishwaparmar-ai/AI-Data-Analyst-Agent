from backend.agents.data_understanding_agent import DataUnderstandingAgent

cleaner = DataUnderstandingAgent()

df = cleaner.read_dataset("uploads/ecommerce_data.csv")

report = cleaner.analyze_dataset(df)

print(report)
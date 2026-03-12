import pandas as pd
df = pd.read_csv('reports/baseline_results.csv')
for disease in df['Disease'].unique():
    print(f"\n--- {disease} ---")
    print(df[df['Disease'] == disease][['Model', 'Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC']])

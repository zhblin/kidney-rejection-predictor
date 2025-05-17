
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import joblib

genes = ['FAM26F.1', 'GPR171', '229668_at', 'B2M.2', 'FAXDC2', 'CCL4', 'CXCL11', 'SOST']

try:
    model = joblib.load("model.pkl")
except:
    raise RuntimeError("❌ Failed to load model.pkl. Please make sure it exists in the current folder.")

root = tk.Tk()
root.title("Kidney Rejection Prediction - Manual Input")
root.geometry("500x500")

entries = {}

tk.Label(root, text="Enter hub gene expression values below:", font=("Arial", 12)).pack(pady=10)

form_frame = tk.Frame(root)
form_frame.pack(pady=5)
for gene in genes:
    row = tk.Frame(form_frame)
    label = tk.Label(row, text=gene, width=15, anchor='w')
    entry = tk.Entry(row, width=20)
    row.pack(side=tk.TOP, fill=tk.X, padx=10, pady=2)
    label.pack(side=tk.LEFT)
    entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries[gene] = entry

def predict():
    try:
        input_values = [float(entries[gene].get()) for gene in genes]
        input_df = pd.DataFrame([input_values], columns=genes)
        prob = model.predict_proba(input_df)[0, 1]
        risk = "🔴 High Risk" if prob > 0.5 else "🟢 Low Risk"
        result_msg = f"Rejection Probability: {prob:.3f}\\nRisk Level: {risk}"
        messagebox.showinfo("Prediction Result", result_msg)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input or model error:\n{{e}}")

tk.Button(root, text="Predict Rejection Risk", command=predict, width=30, height=2, bg="#4CAF50", fg="white").pack(pady=20)

root.mainloop()

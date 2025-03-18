import tkinter as tk
from tkinter import ttk

class GradeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Grade Calculator")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, expand=True, fill='both')

        # Create tabs
        self.create_average_tab()
        self.create_components_tab()
        self.create_prediction_tab()

    def create_average_tab(self):
        # Average grade tab
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Grade Average")
        
        # Widgets
        ttk.Label(frame, text="Enter grades separated by commas:").pack(pady=5)
        self.entry_grades = ttk.Entry(frame, width=40)
        self.entry_grades.pack(pady=5)
        
        ttk.Button(frame, text="Calculate Average", command=self.calculate_average).pack(pady=5)
        self.label_result_average = ttk.Label(frame, text="")
        self.label_result_average.pack(pady=5)

    def create_components_tab(self):
        # Component-based grade tab
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Component Grade")
        
        # Widgets
        instructions = """Enter each component in the format:
Component Name, Weight (%), Grade1 Grade2 Grade3...
Example:
Homework, 30, 85 90 88
Exams, 70, 78 92"""
        ttk.Label(frame, text=instructions).pack(pady=5)
        
        self.text_components = tk.Text(frame, height=10, width=50)
        self.text_components.pack(pady=5)
        
        ttk.Button(frame, text="Calculate Overall Grade", command=self.calculate_components).pack(pady=5)
        self.label_result_components = ttk.Label(frame, text="")
        self.label_result_components.pack(pady=5)

    def create_prediction_tab(self):
        # Score prediction tab
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Score Prediction")
        
        # Widgets
        ttk.Label(frame, text="Current Grade (%):").pack(pady=5)
        self.entry_current = ttk.Entry(frame)
        self.entry_current.pack(pady=5)
        
        ttk.Label(frame, text="Desired Grade (%):").pack(pady=5)
        self.entry_desired = ttk.Entry(frame)
        self.entry_desired.pack(pady=5)
        
        ttk.Label(frame, text="Remaining Weight (%):").pack(pady=5)
        self.entry_remaining = ttk.Entry(frame)
        self.entry_remaining.pack(pady=5)
        
        ttk.Button(frame, text="Calculate Required Score", command=self.calculate_prediction).pack(pady=10)
        self.label_result_prediction = ttk.Label(frame, text="")
        self.label_result_prediction.pack(pady=5)

    def calculate_average(self):
        try:
            grades = [float(g.strip()) for g in self.entry_grades.get().split(',')]
            average = sum(grades) / len(grades)
            self.label_result_average.config(text=f"Average Grade: {average:.2f}%")
        except:
            self.label_result_average.config(text="Invalid input. Please enter grades separated by commas.")

    def calculate_components(self):
        try:
            total_weight = 0.0
            overall_grade = 0.0
            lines = self.text_components.get("1.0", tk.END).strip().split('\n')
            
            for line in lines:
                if not line.strip():
                    continue
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 3:
                    raise ValueError(f"Invalid format in line: {line}")
                
                name = parts[0]
                weight = float(parts[1].strip('% ')) / 100
                grades = list(map(float, parts[2].split()))
                
                category_avg = sum(grades) / len(grades)
                overall_grade += category_avg * weight
                total_weight += weight
            
            if abs(total_weight - 1.0) > 0.001:
                self.label_result_components.config(
                    text=f"Overall Grade: {overall_grade:.2f}% (Warning: Total weight {total_weight*100:.1f}%)")
            else:
                self.label_result_components.config(text=f"Overall Grade: {overall_grade:.2f}%")
        except Exception as e:
            self.label_result_components.config(text=f"Error: {str(e)}")

    def calculate_prediction(self):
        try:
            current = float(self.entry_current.get().strip('% ')) / 100
            desired = float(self.entry_desired.get().strip('% ')) / 100
            remaining = float(self.entry_remaining.get().strip('% ')) / 100
            
            if remaining <= 0:
                raise ValueError("Remaining weight must be greater than 0%")
            
            required = (desired - current * (1 - remaining)) / remaining
            required_percent = required * 100
            
            if required < 0:
                result = "You need 0% on remaining to achieve your goal"
            elif required > 1:
                result = "Desired grade is impossible with current grades"
            else:
                result = f"Minimum required score: {required_percent:.2f}%"
            
            self.label_result_prediction.config(text=result)
        except Exception as e:
            self.label_result_prediction.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculator(root)
    root.mainloop()
import tkinter as tk
from TheShuntingYard import evaluate_expression


def update_expression(symbol):
    current_text = expression_label["text"]
    new_text = current_text + str(symbol)
    expression_label.config(text=new_text)


def clear_expression():
    expression_label.config(text="")


def delete_last_char():
    current_text = expression_label["text"]
    expression_label.config(text=current_text[:-1])


def evaluate():
    try:
        current_text = expression_label["text"]
        result = evaluate_expression(current_text)
        expression_label.config(text=str(result))
    except Exception as e:
        expression_label.config(text="Error")


root = tk.Tk()
root.title("Calculator")
root.geometry("400x300")

expression_label = tk.Label(root, text="", anchor="e", bg="white", fg="black", font=("Arial", 24), relief="sunken")
expression_label.grid(row=0, column=0, columnspan=4, sticky="nsew")

buttons = [
    'C', '(', ')', '/',
    '7', '8', '9', '*',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '0', '.', '^', '=',
    'DEL'
]

row_val = 1
col_val = 0
for button in buttons:
    if button == "C":
        action = clear_expression
    elif button == "=":
        action = evaluate
    elif button == "DEL":
        action = delete_last_char
    else:
        action = lambda x=button: update_expression(x)

    tk.Button(root, text=button, command=action, font=("Arial", 18)).grid(row=row_val, column=col_val, sticky="nsew")

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Run the main loop
root.mainloop()

import argparse
import json
from datetime import datetime

# Archivo para almacenar los datos
DATA_FILE = "expenses.json"

# Función para cargar datos del archivo
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Función para guardar datos en el archivo
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Función para agregar un gasto
def add_expense(expenses, description, amount):
    if amount <= 0:
        print("El monto debe ser mayor que cero.")
        return

    new_id = len(expenses) + 1
    date = datetime.now().strftime("%Y-%m-%d")
    expense = {
        "id": new_id,
        "date": date,
        "description": description,
        "amount": amount
    }
    expenses.append(expense)
    print(f"Gasto agregado exitosamente (ID: {new_id})")

# Función para eliminar un gasto
def delete_expense(expenses, expense_id):
    for i, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            del expenses[i]
            print(f"Gasto eliminado exitosamente (ID: {expense_id})")
            return
    print("Gasto no encontrado.")

# Función para listar todos los gastos
def list_expenses(expenses):
    if not expenses:
        print("No hay gastos registrados.")
        return

    print(f"{'ID':<5} {'Fecha':<12} {'Descripción':<20} {'Monto':<10}")
    print("-" * 50)
    for expense in expenses:
        print(f"{expense['id']:<5} {expense['date']:<12} {expense['description']:<20} ${expense['amount']:<10.2f}")

# Función para mostrar el resumen de gastos
def show_summary(expenses, month=None):
    total = 0
    filtered_expenses = expenses

    if month:
        current_year = datetime.now().year
        filtered_expenses = [e for e in expenses if int(e["date"].split("-")[1]) == month and int(e["date"].split("-")[0]) == current_year]

    for expense in filtered_expenses:
        total += expense["amount"]

    if month:
        print(f"Total de gastos para el mes {month}: ${total:.2f}")
    else:
        print(f"Total de gastos: ${total:.2f}")

# Función principal
def main():
    parser = argparse.ArgumentParser(description="Aplicación de seguimiento de gastos.")
    subparsers = parser.add_subparsers(dest="command")

    # Comando para agregar un gasto
    add_parser = subparsers.add_parser("add", help="Agregar un nuevo gasto")
    add_parser.add_argument("--description", required=True, help="Descripción del gasto")
    add_parser.add_argument("--amount", type=float, required=True, help="Monto del gasto")

    # Comando para eliminar un gasto
    delete_parser = subparsers.add_parser("delete", help="Eliminar un gasto")
    delete_parser.add_argument("--id", type=int, required=True, help="ID del gasto a eliminar")

    # Comando para listar todos los gastos
    subparsers.add_parser("list", help="Mostrar todos los gastos")

    # Comando para ver el resumen de gastos
    summary_parser = subparsers.add_parser("summary", help="Ver resumen de gastos")
    summary_parser.add_argument("--month", type=int, help="Filtrar por mes (número del mes)")

    args = parser.parse_args()

    expenses = load_data()

    if args.command == "add":
        add_expense(expenses, args.description, args.amount)
    elif args.command == "delete":
        delete_expense(expenses, args.id)
    elif args.command == "list":
        list_expenses(expenses)
    elif args.command == "summary":
        show_summary(expenses, args.month)
    else:
        parser.print_help()

    # Guarda los cambios después de cada operación
    save_data(expenses)

if __name__ == "__main__":
    main()
# Copyright (c) 2025, Kareem and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

class EmployeeExpenseClaim(Document):
    def validate(self):
        employee = frappe.get_doc("Employee", self.employee)

        expense_data = {}
        for expense in employee.employee_expense:
            expense_data[expense.expense_claim_type] = {
                "amount_per_km": expense.amount_per_km,
                "pincode": expense.pincode
            }

        for detail in self.employee_expense_claim_details:
            if detail.expense_claim_type == "Food":
                if detail.expense_claim_type in expense_data:
                    pincode = expense_data[detail.expense_claim_type]["pincode"]
                    if not pincode:
                        frappe.throw("Pincode not specified for Food in Employee's expense data.")

                    pincode_doc = frappe.get_doc("Pincode", pincode)
                    max_food_amount = pincode_doc.amount  

                    if detail.amount > max_food_amount:
                        frappe.throw(
                            f"The Food-related amount ({detail.amount}) exceeds the allowed limit "
                            f"for Pincode {pincode} ({max_food_amount})."
                        )
                else:
                    frappe.throw(f"Expense Claim Type 'Food' not found for the selected employee.")
            else:
                if detail.expense_claim_type in expense_data:
                    calculated_amount = detail.distance_in_km * expense_data[detail.expense_claim_type]["amount_per_km"]
                    detail.amount = calculated_amount
                else:
                    frappe.throw(f"Expense Claim Type '{detail.expense_claim_type}' not found for the selected employee.")

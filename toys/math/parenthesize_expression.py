#!/usr/bin/env python


def evaluate(expression):
    try:
        return eval(expression)
    except Exception as e:
        return float("nan")


def generate_parenthesizations(expression):
    if expression.isdigit():
        return [expression]

    result = []
    for i in range(len(expression)):
        if expression[i] in "+-*/":
            left = generate_parenthesizations(expression[:i])
            right = generate_parenthesizations(expression[i + 1 :])
            for l in left:
                for r in right:
                    result.append(f"({l}{expression[i]}{r})")
    return result


def main(expression):
    parenthesizations = generate_parenthesizations(expression.replace(" ", ""))
    parenthesizations.sort(key=evaluate)
    for i, expr in enumerate(parenthesizations, 1):
        if expr.startswith("(") and expr.endswith(")"):
            expr = expr[1:-1]
        value = evaluate(expr)
        print(f"{i}: {expr} = {value}")


expression = input("Enter expression [2*3-4*5]:")
if not expression:
    expression = "2*3-4*5"
print()
main(expression)

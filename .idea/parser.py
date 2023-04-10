import re
from abc import ABC, abstractmethod
import math
from numpy import double


class Expression(ABC):
    """
    Abstract base class for arithmetic expressions.
    """
    @abstractmethod
    def calc(self) -> double:
        """
        Abstract method for evaluating the expression and returning the result.
        """
        pass
class Num(Expression):
    """
    Class for representing numeric values in arithmetic expressions.
    """
    def __init__(self, value):
        """
        Constructor for initializing the numeric value.
        """
        self.value = value
    def set_value(self, value: double):
        """
        Set class value (double)
        """
        self.value = value

    def calc(self) -> double:
        """
        Method for returning the numeric value.
        """
        return self.value
class BinaryExpression(Expression):
    """
    Class for representing binary operations in arithmetic expressions.
    """
    def __init__(self, left: Expression, right: Expression):
        """
        Constructor for initializing the left and right operands of the binary operation.
        """
        self.left = left
        self.right = right
    def calc(self) -> double:
        """
        Abstract method for evaluating the binary operation and returning the result.
        """
        pass
class Plus(BinaryExpression):
    """
    Class for representing addition operations in arithmetic expressions.
    """
    def __init__(self, left: Expression, right: Expression):
        """
        Constructor for initializing the left and right operands of the addition operation.
        """
        super().__init__(left, right)
        self.left = left
        self.right = right
    def calc(self) -> double:
        """
        Method for evaluating the addition operation and returning the result.
        """
        if hasattr(self.right, 'value'):
            return double(self.left.value) + double(self.right.value)
        return double(self.left.value) + double(self.right.calc())
class Minus(BinaryExpression):
    """
    Class for representing subtraction operations in arithmetic expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        """
        Constructor for initializing the left and right operands of the subtraction operation.
        """
        super().__init__(left, right)
        self.left = left
        self.right = right

    def calc(self) -> double:
        """
        Method for evaluating the subtraction operation and returning the result.
        """
        return double(self.left.value) - double(self.right.value)
class Mul(BinaryExpression):
    """
    Class for representing multiplication operations in arithmetic expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        """
        Constructor for initializing the left and right operands of the multiplication operation.
        """
        super().__init__(left, right)
        self.left = left
        self.right = right

    def calc(self) -> double:
        """
        Method for evaluating the multiplication operation and returning the result.
        """
        if hasattr(self.right, 'value'):
            return double(self.left.value) * double(self.right.value)
        return double(self.left.value) * double(self.right.calc())
class Div(BinaryExpression):
    """
    Class for representing division operations in arithmetic expressions.
    """

    def __init__(self, left: Expression, right: Expression):
        """
        Constructor for initializing the left and right operands of the division operation.
        """
        super().__init__(left, right)
        self.left = left
        self.right = right

    def calc(self) -> double:
        """
        Method for evaluating the division operation and returning the result.
        """
        return double(self.left.value) / double(self.right.value)


def parser(expression) -> float:
    """
    Evaluates a mathematical expression and returns its result as a double.

    Args:
        expression (str): a string containing a mathematical expression to be evaluated

    Returns:
        float: the result of the evaluated expression

    Raises:
        ValueError: if the expression is invalid or cannot be evaluated

    Examples:
        >>> parser('2 + 3 * 4')
        14.0
        >>> parser('(2 + 3) * 4')
        20.0
    """

    operator_stack = []
    operand_queue = []
    components = []
    stack = []
    operator_precedence = {'+': 1,'-': 1,'*': 2,'/': 2,'%': 2}

    # Step 1: Split the expression into its components
    components = re.split(' *([+\-*/()]|\d+\.\d+|\d+) *', expression)
    components = [c for c in components if c != '']

    # Handle negative numbers
    for i in range(len(components) - 1):
        if components[0] == '-':
            components[1] = '-1' + components[1]
        elif components[i] in ('+', '-', '*', '/', '(') and components[i + 1] == '-':
            components[i + 2] = '-' + components[i + 2]
            components[i + 1] = ''
    components = [c for c in components if c != '']

    # Step 2: Convert the components into postfix notation
    for component in components:
        # If component is an operator, handle accordingly
        if component in ('+', '-', '*', '/'):
            # Pop operators from stack and add to queue until precedence of current operator is lower or equal
            while operator_stack and operator_stack[-1] != '(' and operator_precedence.get(component, 0) <= operator_precedence.get(operator_stack[-1], 0):
                operand_queue.append(operator_stack.pop())
            # Push the current operator to the stack
            operator_stack.append(component)
        # If component is an opening parenthesis, push to operator stack
        elif component == '(':
            operator_stack.append(component)
        # If component is a closing parenthesis, pop operators from stack and add to queue until matching opening parenthesis
        elif component == ')':
            while operator_stack and operator_stack[-1] != '(':
                operand_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()
        # If component is a number, push to operand queue
        else:
            operand_queue.append(double(component))

    # Pop remaining operators from stack and add to queue
    while operator_stack:
        operand_queue.append(operator_stack.pop())

    # Step 3: Evaluate the postfix notation
    for d in operand_queue:
        if d not in ('+', '-', '*', '/'):
            stack.append(double(d))
        else:
            # Pop the top two operands and apply the operator
            right = stack.pop()
            left = stack.pop()

            if d == '+':
                stack.append(left + right)
            elif d == '-':
                stack.append(left - right)
            elif d == '*':
                stack.append(left * right)
            elif d == '/':
                stack.append(left / right)

    return double(stack.pop())

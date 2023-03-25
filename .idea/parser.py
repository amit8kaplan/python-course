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


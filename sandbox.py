from dataclasses import dataclass


@dataclass
class A():
    x: int

    def __eq__(self, other):
        if isinstance(other, int):
            return NotImplemented
        return True


a = A(1)
b = 1

print(a == b)
print(b == a)

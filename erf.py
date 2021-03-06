import math
from array import array
from integral import integral


class Erf:
    def __init__(self):
        self.derivative = lambda x: 2 / math.sqrt(math.pi) * math.exp(-x**2)

    def taylor(self, x, eps=1e-6):
        a = x
        erf = x
        q = self.quotient(x, 0)
        n = 0
        while abs(a) > eps:
            a *= q
            erf += a
            n += 1
            q = self.quotient(x, n)
        return (2 / math.sqrt(math.pi)) * erf

    def lagrange(self, nodes, values, x):
        Ln = 0
        for i in range(0, len(nodes)):
            F = 1
            for j in range(0, len(nodes)):
                if i != j:
                    F *= (x - nodes[j]) / (nodes[i] - nodes[j])
            Ln += values[i] * F
        return Ln

    def lagrange_for_derivative(self, nodes, values, x):
        Ln = 0
        n = len(nodes)
        p = 1
        lk = 0

        for k in range(0, n):
            for j in range(0, n):
                if j != k:
                    p = 1
                    for i in range(0, n):
                        if i != k and i != j:
                            p *= (x - nodes[i]) / (nodes[k] - nodes[i])
                    p /= nodes[k] - nodes[j]
                    lk += p
            Ln += values[k] * lk
            lk = 0
        return Ln

    # methods: gauss, simpson, left_rectangle, center_rectangle, trapezoidal
    def integral(self, x, method = 'left_rectangle', eps = 1e-4):
        prev, current = integral(self.derivative, 0, x, 1, method), integral(self.derivative, 0, x, 2, method)
        tmp = current
        N = 2
        while abs(prev - current) > eps:
            N *= 2
            current = integral(self.derivative, 0, x, N, method)
            prev = tmp
            tmp = current
        return N

    def inverse(self, f, eps = 1e-6):
        x_prev = 0.2
        x_current = x_prev - (self.taylor(x_prev) - f) / self.derivative(x_prev)
        x_next = 0
        while abs(self.taylor(x_current) - f) > eps:
            g_x_current = self.taylor(x_current) - f
            g_derivative_x_current = self.derivative(x_current)
            g_derivative_x_prev = self.derivative(x_prev)
            x_next = x_current - g_x_current / g_derivative_x_current - 0.5 * (g_x_current ** 2 / g_derivative_x_current ** 3) * ((g_derivative_x_current - g_derivative_x_prev) / (x_current - x_prev))
            x_prev = x_current
            x_current = x_next
        return x_current

    # helper method for calc one node, after "overload" for scalar and list

    def quotient(self, x, n):
        return (-x * x * (2 * n + 1)) / ((n + 1) * (2 * n + 3))

if __name__ == '__main__':
    main()

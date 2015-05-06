import erf
import compare
import nodes

f = erf.Erf()

# helper methods
def write_tab_line(a, digits, out):
    counter = 0
    rounding = '%.' + str(digits) + 'f'
    n = len(a)
    for x in a:
        counter += 1
        out.write('$' + rounding % x + '$' + ('&' if counter < n else '\\\\\n'))
    return

def tex_siquence(arr):
    return str(arr[0]) + ', ' + str(arr[1]) + '\\dots' + str(arr[len(arr) - 1])

# formulagte report files
def taylor(a, b, n):
    out = open('./tex/taylor.tex', 'w')
    out.write('Протабулируем $erf(x)$ на отрезке [' + str(a) + ', ' + str(b) + '] на ' + str(n) + ' узлах с точностью $10^{-6}$, основываясь на ряде Тейлора:\\\\\n')
    out.write('\\begin{tabular}{' + 'c'*(n+1) + '}\n')
    taylor_nodes = nodes.equidistant_nodes(a, b, n)
    values = nodes.method_for_array(taylor_nodes, f.taylor)
    out.write('\hline\n')
    write_tab_line(taylor_nodes, 2, out)
    out.write('\hline\n')
    write_tab_line(values, 6, out)
    out.write('\\end{tabular}')

def lagrange_max_error(a, b):
    out = open('./tex/lagrange.tex', 'w')
    nodes_count = []
    chebyshev = []
    equidistant = []
    for i in range(8):
        nodes_count.append(8 + 2*i)
    for count in nodes_count:
        chebyshev.append(compare.chebyshev_max_error(a, b, f.lagrange, f.taylor, count))
        equidistant.append(compare.equidistant_max_error(a, b, f.lagrange, f.taylor, count))
    out.write('Протабулируем $L_n(x)$ на отрезке [' + str(a) + ', ' + str(b) + '], где $n =' + tex_siquence(nodes_count) + '$ и вычилим погрешность в равностоящих $2n$ узлах\\\\\n')
    out.write('\\begin{tabular}{' + 'r|' + 'c'*len(nodes_count) + '}\n')
    out.write('\hline\n')
    out.write('Кол-во узлов&')
    write_tab_line(nodes_count, 0, out)
    out.write('\hline\n')

    out.write('равн. узлы&')
    write_tab_line(equidistant, 8, out)
    out.write('Чеб. узлы&')
    write_tab_line(chebyshev, 8, out)
    out.write('\\end{tabular}')

def derivative_of_lagrange_max_error(a, b):
    out = open('./tex/derivative_of_lagrange_max_error.tex', 'w')
    nodes_count = []
    chebyshev = []
    equidistant = []
    for i in range(8):
        nodes_count.append(8 + 2*i)
    for count in nodes_count:
        chebyshev.append(compare.chebyshev_max_error(a, b, f.lagrange_for_derivative, f.derivative, count))
        equidistant.append(compare.equidistant_max_error(a, b, f.lagrange_for_derivative, f.derivative, count))
    out.write('Протабулируем $L’_n(x)$ на отрезке [' + str(a) + ', ' + str(b) + '], где $n =' + tex_siquence(nodes_count) + '$ и вычилим погрешность в равностоящих $2n$ узлах\\\\\n')
    out.write('\\begin{tabular}{' + 'r|' + 'c'*len(nodes_count) + '}\n')
    out.write('\hline\n')
    out.write('Кол-во узлов&')
    write_tab_line(nodes_count, 0, out)
    out.write('\hline\n')

    out.write('равн. узлы&')
    write_tab_line(equidistant, 8, out)
    out.write('Чеб. узлы&')
    write_tab_line(chebyshev, 8, out)
    out.write('\\end{tabular}\n\n')

def derivative_of_lagrange_errors(a, b, n, out):
    points = nodes.equidistant_nodes(a, b, 2*n)
    out.write('\\quad\n\\noindent Количество узлов интерполяции - ' + str(n) + '. Считаем в равноудаленных ' + str(2*n) + ' узлах.\\\\\n')
    chebyshev = compare.chebyshev_errors(a, b, f.lagrange_for_derivative, f.derivative, n)
    equidistant = compare.equidistant_errors(a, b, f.lagrange, f.taylor, n)
    out.write('\\begin{tabular}{ccc}\n')
    out.write('\hline\n')
    out.write('$x$&Погрешность(Чеб. узлы)&Погрешность (ровн. узлы)\\\\\n')
    out.write('\hline\n')
    for i in range(2*n):
        arr = [points[i], chebyshev[i], equidistant[i]]
        write_tab_line(arr, 8, out)
    out.write('\hline\n')
    out.write('\\end{tabular}\\\\\n\n')

def derivative(a, b):
    out = open('./tex/derivative_errors.tex', 'w')
    derivative_of_lagrange_errors(a, b, 8, out)
    derivative_of_lagrange_errors(a, b, 16, out)
    derivative_of_lagrange_max_error(a, b)



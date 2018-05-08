from ortools.linear_solver import pywraplp

def solve_problem(num_vertices, edges, debug=False ):
    solver = pywraplp.Solver("Graph Coloring", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    # what if we use one variable per vertex
    # values -- 1..5

    # does it make sense to prime with some sort of solution

    num_colors = 50
    # every vertex will get a color
    v_color_array = {}
    for i in range(0,num_colors):
        for x in range(num_vertices):
            v_color_array[x, i] = solver.IntVar(0,1,"v_{}_c_{}".format(x,i))

    # this is a cool way to see whether color is used
    u = [solver.IntVar(0, 1, 'u[%i]' % i) for i in range(num_colors)]
    # minimize total number of colors used
    o_func = solver.Sum(u)

    # Each node needs some color assigned
    for v in range(0, num_vertices):
        solver.Add(solver.Sum ( [ v_color_array[v,c] for c in range(0,num_colors)] ) == 1 )

    # this is done instead of directly comparing values is that
    # both can be 0 ( which is ok since color is not used)
    for v0,v1 in edges:
        for c in range(num_colors):
            solver.Add(v_color_array[v0, c] + v_color_array[v1,c] <= u[c])

    #objective = solver.Minimize(o_func)
    solver.Solve()

    if debug:
        print()
        print('number of colors:', int(solver.Objective().Value()))
        print('colors used:', [int(u[i].SolutionValue()) for i in range(num_colors)])
        print()

    solution = []
    for v in range(0, num_vertices):
        if debug:
            print("v{}_color".format(v))
        for c in range(num_colors):
            if int(v_color_array[v, c].SolutionValue()) == 1:
                if debug:
                    print(c)
                solution.append(c)

    replace = {}
    for x,y in enumerate(set(solution)):
        replace[y] = x
    xx  = list( map( lambda x: replace[x], solution ) )
    return xx
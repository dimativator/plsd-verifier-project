import sys

n = int(input())
g = [int(i) - 1 for i in sys.stdin.readline().split()]


def solve(n, g):
    vertex_id = [-1]*n
    current_id = 0

    cycle_starts = []
    cycle_starts_by_vertex = [-1]*n
    cycle_vertex_sample = []
    start_on_cycle = []

    cycle_index_by_ID = []

    for v in range(n):
        if vertex_id[v] != -1: continue

        current_vertex = v
        cycle_found = False
        while vertex_id[current_vertex] == -1:
            vertex_id[current_vertex] = current_id
            current_vertex = g[current_vertex]

            if vertex_id[current_vertex] == current_id:
                cycle_found = True
                # cycle_starts.append([v])                
                cycle_vertex_sample.append(current_vertex)
                start_on_cycle.append(current_vertex == v)



        if not cycle_found:
            if cycle_starts_by_vertex[current_vertex] != -1:
                cycle_starts_by_vertex[v] = cycle_starts_by_vertex[current_vertex]
                cycle_starts_by_vertex[current_vertex] = -1
            cycle_index_by_ID.append(cycle_index_by_ID[vertex_id[current_vertex]])

            cycle = cycle_index_by_ID[-1]

            if start_on_cycle[cycle]:
                cycle_starts_by_vertex[cycle_vertex_sample[cycle]] = -1
                start_on_cycle[cycle] = False
                # cycle_starts[cycle] = []

            cycle_starts_by_vertex[v] = cycle
                
            # starts = cycle_starts[cycle]
            # for i in range(len(starts)):
            #     if starts[i] == current_vertex:
            #         starts[i] = v
            #         break
            # else:
            #     starts.append(v)

        else:
            cycle_starts_by_vertex[v] = len(cycle_vertex_sample) - 1
            cycle_index_by_ID.append(len(cycle_vertex_sample) - 1)
        current_id += 1

    cycle_starts = [[] for _ in range(len(cycle_vertex_sample))]
    for i in range(n):
        if cycle_starts_by_vertex[i] != -1:
            cycle_starts[cycle_starts_by_vertex[i]].append(i)


    expanded = []
    for i in range(len(cycle_vertex_sample)):
        v = cycle_vertex_sample[i]
        for u in cycle_starts[i]:
            expanded.append([v, u])

    if len(expanded) == 1 and expanded[0][0] == expanded[0][1]:
        print(0)
    else:
        ans = []
        for i in range(len(expanded)-1):
            v = expanded[i][0]
            u = expanded[i+1][1]
            ans.append('{0} {1}'.format(v+1, u+1))
        ans.append('{0} {1}'.format(expanded[-1][0] + 1, expanded[0][1] + 1))

        print(len(ans))
        print('\n'.join(ans)) 

solve(n, g)
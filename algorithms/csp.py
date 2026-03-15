from __future__ import annotations
from collections import deque

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from algorithms.problems_csp import DroneAssignmentCSP


def backtracking_search(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Basic backtracking search without optimizations.

    Tips:
    - An assignment is a dictionary mapping variables to values (e.g. {X1: Cell(1,2), X2: Cell(3,4)}).
    - Use csp.assign(var, value, assignment) to assign a value to a variable.
    - Use csp.unassign(var, assignment) to unassign a variable.
    - Use csp.is_consistent(var, value, assignment) to check if an assignment is consistent with the constraints.
    - Use csp.is_complete(assignment) to check if the assignment is complete (all variables assigned).
    - Use csp.get_unassigned_variables(assignment) to get a list of unassigned variables.
    - Use csp.domains[var] to get the list of possible values for a variable.
    - Use csp.get_neighbors(var) to get the list of variables that share a constraint with var.
    - Add logs to measure how good your implementation is (e.g. number of assignments, backtracks).

    You can find inspiration in the textbook's pseudocode:
    Artificial Intelligence: A Modern Approach (4th Edition) by Russell and Norvig, Chapter 5: Constraint Satisfaction Problems
    """
    
    #Primera Versión, sin ayuda de IA:
    """
    def backtrack(assignment):
        if csp.is_complete(assignment):
            return assignment

        var = csp.get_unassigned_variables(assignment)[0]

        for value in csp.domains[var]:
            if csp.is_consistent(var, value, assignment):
                csp.assign(var, value, assignment)

                result = backtrack(assignment)
                if result is not None:
                    return result

                csp.unassign(var, assignment)

        return None

    return backtrack({})
    """
    #Prompt utilizado para mejorar el código creado en un principio (ChatGPT - 5.3):
    """
    Estoy haciendo un taller de Inteligencia Artificial y tengo que implementar backtracking_search para un CSP llamado DroneAssignmentCSP. 
    La idea es que sea el backtracking básico del libro de Russell & Norvig, sin heurísticas ni optimizaciones raras.

    Ya tengo una primera versión que funciona, pero es bastante básica y quiero mejorarla un poco manteniendo la misma lógica y estilo del código. 
    Esta es la versión que tengo ahora: 
    
    def backtrack(assignment):
        if csp.is_complete(assignment):
            return assignment

        var = csp.get_unassigned_variables(assignment)[0]

        for value in csp.domains[var]:
            if csp.is_consistent(var, value, assignment):
                csp.assign(var, value, assignment)

                result = backtrack(assignment)
                if result is not None:
                    return result

                csp.unassign(var, assignment)

        return None

    return backtrack({})
    
    Lo que quiero es mantener exactamente este enfoque de backtracking puro, usando una función recursiva interna, sin meter MRV, LCV, forward checking 
    ni AC3 porque esas van en otras funciones del taller. Solo quiero dejar esta versión un poco más completa y limpia.
    
    También me gustaría agregar contadores simples para saber cuántos assignments se hacen y cuántos backtracks ocurren durante la búsqueda, e imprimir 
    esos valores al final para poder comparar luego con otras variantes del algoritmo.
    
    Puedes devolver solo la versión final de la función backtracking_search en Python manteniendo el estilo simple y claro de este código?
    """
    
    #Código Final con ayuda de la IA (ChatGPT - 5.3):

    assignments_count = 0
    backtracks_count = 0

    def backtrack(assignment):
        nonlocal assignments_count, backtracks_count

        if csp.is_complete(assignment):
            return assignment

        var = csp.get_unassigned_variables(assignment)[0]

        for value in csp.domains[var]:
            if csp.is_consistent(var, value, assignment):
                csp.assign(var, value, assignment)
                assignments_count += 1

                result = backtrack(assignment)
                if result is not None:
                    return result

                csp.unassign(var, assignment)

        backtracks_count += 1
        return None

    result = backtrack({})

    print(f"[backtracking_search] assignments: {assignments_count}")
    print(f"[backtracking_search] backtracks: {backtracks_count}")

    return result


def backtracking_fc(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking search with Forward Checking.

    Tips:
    - Forward checking: After assigning a value to a variable, eliminate inconsistent values from
      the domains of unassigned neighbors. If any neighbor's domain becomes empty, backtrack immediately.
    - Save domains before forward checking so you can restore them on backtrack.
    - Use csp.get_neighbors(var) to get variables that share constraints with var.
    - Use csp.is_consistent(neighbor, val, assignment) to check if a value is still consistent.
    - Forward checking reduces the search space by detecting failures earlier than basic backtracking.
    """
    #Primera Versión, sin ayuda de IA:
    """
    def backtrack(assignment):
        if csp.is_complete(assignment):
            return assignment

        var = csp.get_unassigned_variables(assignment)[0]

        for value in csp.domains[var]:
            if csp.is_consistent(var, value, assignment):
                csp.assign(var, value, assignment)

                saved_domains = {v: list(csp.domains[v]) for v in csp.domains}
                failure = False

                for neighbor in csp.get_neighbors(var):
                    if neighbor not in assignment:
                        new_domain = []
                        for val in csp.domains[neighbor]:
                            if csp.is_consistent(neighbor, val, assignment):
                                new_domain.append(val)
                        csp.domains[neighbor] = new_domain

                        if len(csp.domains[neighbor]) == 0:
                            failure = True
                            break

                if not failure:
                    result = backtrack(assignment)
                    if result is not None:
                        return result

                csp.domains = saved_domains
                csp.unassign(var, assignment)

        return None

    return backtrack({})
    """
    
    #Prompt utilizado para mejorar el código creado en un principio (ChatGPT - 5.3):
    """
    Estoy haciendo un taller de Inteligencia Artificial y ahora necesito implementar backtracking_fc para un CSP llamado DroneAssignmentCSP. Esta función 
    debe hacer backtracking con forward checking, pero sin meter otras heurísticas como MRV, LCV o AC3, porque esas van aparte en otras funciones.

    Ya tengo una primera versión beta que intenta hacerlo y quiero mejorarla manteniendo la misma lógica general y un estilo simple, claro y parecido al de 
    un estudiante. Esta es la versión que tengo ahora:

    def backtracking_fc(csp):
        def backtrack(assignment):
            if csp.is_complete(assignment):
                return assignment

            var = csp.get_unassigned_variables(assignment)[0]

            for value in csp.domains[var]:
                if csp.is_consistent(var, value, assignment):
                    csp.assign(var, value, assignment)

                    saved_domains = {v: list(csp.domains[v]) for v in csp.domains}
                    failure = False

                    for neighbor in csp.get_neighbors(var):
                        if neighbor not in assignment:
                            new_domain = []
                            for val in csp.domains[neighbor]:
                                if csp.is_consistent(neighbor, val, assignment):
                                    new_domain.append(val)
                            csp.domains[neighbor] = new_domain

                            if len(csp.domains[neighbor]) == 0:
                                failure = True
                                break

                    if not failure:
                        result = backtrack(assignment)
                        if result is not None:
                            return result

                    csp.domains = saved_domains
                    csp.unassign(var, assignment)

            return None

        return backtrack({})

    Quiero que me devuelvas una versión final más limpia, mejor estructurada y en general mejor, pero manteniendo este mismo enfoque. La implementación debe seguir usando
    una función recursiva interna y debe seguir usando las funciones del objeto csp como assign, unassign, is_consistent, is_complete y get_unassigned_variables. 
    También quiero agregar contadores simples para medir cuántos assignments se hacen, cuántos backtracks ocurren y cuántas veces falla el forward checking, 
    e imprimir esos valores al final. Devuélveme únicamente la implementación final de la función backtracking_fc en Python, manteniendo un estilo simple, claro y natural.
    """
    #Código Final con ayuda de la IA (ChatGPT - 5.3):
    
    assignments_count = 0
    backtracks_count = 0
    fc_failures_count = 0

    def copy_domains():
        return {var: list(values) for var, values in csp.domains.items()}

    def forward_check(var, assignment):
        nonlocal fc_failures_count

        for neighbor in csp.get_neighbors(var):
            if neighbor in assignment:
                continue

            filtered_domain = []
            for value in csp.domains[neighbor]:
                if csp.is_consistent(neighbor, value, assignment):
                    filtered_domain.append(value)

            csp.domains[neighbor] = filtered_domain

            if len(filtered_domain) == 0:
                fc_failures_count += 1
                return False

        return True

    def backtrack(assignment):
        nonlocal assignments_count, backtracks_count

        if csp.is_complete(assignment):
            return assignment

        var = csp.get_unassigned_variables(assignment)[0]

        for value in csp.domains[var]:
            if not csp.is_consistent(var, value, assignment):
                continue

            saved_domains = copy_domains()
            csp.assign(var, value, assignment)
            assignments_count += 1

            if forward_check(var, assignment):
                result = backtrack(assignment)
                if result is not None:
                    return result

            csp.domains = saved_domains
            csp.unassign(var, assignment)

        backtracks_count += 1
        return None

    result = backtrack({})

    print(f"[backtracking_fc] assignments: {assignments_count}")
    print(f"[backtracking_fc] backtracks: {backtracks_count}")
    print(f"[backtracking_fc] forward checking failures: {fc_failures_count}")

    return result

def backtracking_ac3(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking search with AC-3 arc consistency.

    Tips:
    - AC-3 enforces arc consistency: for every pair of constrained variables (Xi, Xj), every value
      in Xi's domain must have at least one supporting value in Xj's domain.
    - Run AC-3 before starting backtracking to reduce domains globally.
    - After each assignment, run AC-3 on arcs involving the assigned variable's neighbors.
    - If AC-3 empties any domain, the current assignment is inconsistent - backtrack.
    - You can create helper functions such as:
      - a values_compatible function to check if two variable-value pairs are consistent with the constraints.
      - a revise function that removes unsupported values from one variable's domain.
      - an ac3 function that manages the queue of arcs to check and calls revise.
      - a backtrack function that integrates AC-3 into the search process.
    """
    """Primera version:
    def backtracking_ac3(csp: DroneAssignmentCSP) -> dict[str, str] | None:

    def values_compatible(xi, vi, xj, vj):
        temp = {xi: vi}
        return csp.is_consistent(xj, vj, temp)

    def revise(xi, xj):
        revised = False
        new_domain = []

        for vi in csp.domains[xi]:
            ok = False
            for vj in csp.domains[xj]:
                if values_compatible(xi, vi, xj, vj):
                    ok = True
                    break
            if ok:
                new_domain.append(vi)
            else:
                revised = True

        csp.domains[xi] = new_domain
        return revised

    def ac3(queue):
        while queue:
            xi, xj = queue.pop(0)

            if revise(xi, xj):
                if len(csp.domains[xi]) == 0:
                    return False

                for xk in csp.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))

        return True

    def backtrack(assignment):

        if csp.is_complete(assignment):
            return assignment

        vars_unassigned = csp.get_unassigned_variables(assignment)
        var = vars_unassigned[0]

        for value in csp.domains[var]:

            if csp.is_consistent(var, value, assignment):

                csp.assign(var, value, assignment)

                old_domains = {v: list(csp.domains[v]) for v in csp.domains}
                csp.domains[var] = [value]

                queue = []
                for neighbor in csp.get_neighbors(var):
                    if neighbor not in assignment:
                        queue.append((neighbor, var))

                if ac3(queue):
                    result = backtrack(assignment)
                    if result is not None:
                        return result

                csp.domains = old_domains
                csp.unassign(var, assignment)

        return None

    queue = []
    for xi in csp.variables:
        for xj in csp.get_neighbors(xi):
            queue.append((xi, xj))

    if not ac3(queue):
        return None

    return backtrack({})

    Prompt usado: Por favor ayudame a completar el código dejandolo más óptimo de lo que ya está
    
    version final a continuacion:
    """
    

    def values_compatible(xi, vi, xj, vj):
        temp_assignment = {xi: vi}
        return csp.is_consistent(xj, vj, temp_assignment)

    def revise(xi, xj):
        revised = False
        domain_xi = csp.domains[xi]
        domain_xj = csp.domains[xj]

        new_domain = []

        for vi in domain_xi:
            has_support = False

            for vj in domain_xj:
                if values_compatible(xi, vi, xj, vj):
                    has_support = True
                    break

            if has_support:
                new_domain.append(vi)
            else:
                revised = True

        if revised:
            csp.domains[xi] = new_domain

        return revised

    def ac3(queue):
        queue = deque(queue)

        while queue:
            xi, xj = queue.popleft()

            if revise(xi, xj):
                if not csp.domains[xi]:
                    return False

                for xk in csp.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))

        return True

    def copy_domains():
        return {var: list(values) for var, values in csp.domains.items()}

    def backtrack(assignment):
        if csp.is_complete(assignment):
            return assignment

        unassigned_vars = csp.get_unassigned_variables(assignment)
        var = unassigned_vars[0]

        for value in list(csp.domains[var]):
            if csp.is_consistent(var, value, assignment):
                saved_domains = copy_domains()

                csp.assign(var, value, assignment)
                csp.domains[var] = [value]

                queue = []
                for neighbor in csp.get_neighbors(var):
                    if neighbor not in assignment:
                        queue.append((neighbor, var))

                if ac3(queue):
                    result = backtrack(assignment)
                    if result is not None:
                        return result

                csp.domains = saved_domains
                csp.unassign(var, assignment)

        return None

    initial_queue = []
    for xi in csp.variables:
        for xj in csp.get_neighbors(xi):
            initial_queue.append((xi, xj))

    if not ac3(initial_queue):
        return None

    return backtrack({})

    


def backtracking_mrv_lcv(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking with Forward Checking + MRV + LCV.

    Tips:
    - Combine the techniques from backtracking_fc, mrv_heuristic, and lcv_heuristic.
    - MRV (Minimum Remaining Values): Select the unassigned variable with the fewest legal values.
      Tie-break by degree: prefer the variable with the most unassigned neighbors.
    - LCV (Least Constraining Value): When ordering values for a variable, prefer
      values that rule out the fewest choices for neighboring variables.
    - Use csp.get_num_conflicts(var, value, assignment) to count how many values would be ruled out for neighbors if var=value is assigned.
    """
    """
    Primera versión: Pseudocodigo
    def backtracking_mrv_lcv(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    # idea general:
    # 1. si la asignación está completa, devolverla
    # 2. escoger la variable no asignada con MRV
    #    - la que tenga menos valores legales posibles
    #    - si hay empate, usar degree heuristic
    # 3. ordenar los valores del dominio con LCV
    #    - primero los que menos conflictos generen
    # 4. probar cada valor:
    #    - si es consistente, asignarlo
    #    - guardar copia de dominios
    #    - hacer forward checking sobre vecinos
    #    - si ningún dominio queda vacío, seguir recursivamente
    #    - si falla, restaurar dominios y desasignar
    # 5. si nada sirve, devolver None
    pass
    
    Luego, se hizo una primera implementación ignorando estilo y eficiencia:
    def backtracking_mrv_lcv(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    def backtrack(assignment):
        # 1. si la asignación está completa, devolverla
        if csp.is_complete(assignment):
            return assignment

        # 2. escoger variable no asignada con MRV
        unassigned = csp.get_unassigned_variables(assignment)

        best_var = None
        best_count = None
        best_degree = None

        for var in unassigned:
            legal_count = 0
            for value in csp.domains[var]:
                if csp.is_consistent(var, value, assignment):
                    legal_count += 1

            degree = 0
            for neighbor in csp.get_neighbors(var):
                if neighbor not in assignment:
                    degree += 1

            if best_var is None:
                best_var = var
                best_count = legal_count
                best_degree = degree
            else:
                if legal_count < best_count:
                    best_var = var
                    best_count = legal_count
                    best_degree = degree
                elif legal_count == best_count:
                    if degree > best_degree:
                        best_var = var
                        best_count = legal_count
                        best_degree = degree

        var = best_var

        # 3. ordenar valores del dominio con LCV
        value_conflicts = []

        for value in csp.domains[var]:
            conflicts = 0
            temp_assignment = assignment.copy()
            temp_assignment[var] = value

            for neighbor in csp.get_neighbors(var):
                if neighbor not in assignment:
                    for neighbor_value in csp.domains[neighbor]:
                        if not csp.is_consistent(neighbor, neighbor_value, temp_assignment):
                            conflicts += 1

            value_conflicts.append((value, conflicts))

        value_conflicts.sort(key=lambda x: x[1])

        ordered_values = []
        for pair in value_conflicts:
            ordered_values.append(pair[0])

        # 4. probar cada valor
        for value in ordered_values:
            if csp.is_consistent(var, value, assignment):
                csp.assign(var, value, assignment)

                # guardar copia de dominios
                old_domains = {}
                for x in csp.domains:
                    old_domains[x] = list(csp.domains[x])

                # forward checking
                failed = False
                for neighbor in csp.get_neighbors(var):
                    if neighbor not in assignment:
                        new_domain = []
                        for neighbor_value in csp.domains[neighbor]:
                            if csp.is_consistent(neighbor, neighbor_value, assignment):
                                new_domain.append(neighbor_value)

                        csp.domains[neighbor] = new_domain

                        if len(new_domain) == 0:
                            failed = True

                # si ningún dominio queda vacío, seguir recursivamente
                if not failed:
                    result = backtrack(assignment)
                    if result is not None:
                        return result

                # si falla, restaurar dominios y desasignar
                csp.domains = old_domains
                csp.unassign(var, assignment)

        # 5. si nada sirve, devolver None
        return None

    return backtrack({})


    Finalmente, se realizo la siguiente consulta a ChatGPT:
    "Por favor refinale eficiencia y estilo"
    Dando esta como version definitiva

    """

    def count_legal_values(var, assignment):
        count = 0
        for value in csp.domains[var]:
            if csp.is_consistent(var, value, assignment):
                count += 1
        return count

    def count_unassigned_neighbors(var, assignment):
        count = 0
        for neighbor in csp.get_neighbors(var):
            if neighbor not in assignment:
                count += 1
        return count

    def select_unassigned_variable(assignment):
        unassigned = csp.get_unassigned_variables(assignment)

        return min(
            unassigned,
            key=lambda var: (
                count_legal_values(var, assignment),
                -count_unassigned_neighbors(var, assignment),
            ),
        )

    def order_domain_values(var, assignment):
        def lcv_score(value):
            temp_assignment = assignment.copy()
            temp_assignment[var] = value
            conflicts = 0

            for neighbor in csp.get_neighbors(var):
                if neighbor in assignment:
                    continue

                for neighbor_value in csp.domains[neighbor]:
                    if not csp.is_consistent(
                        neighbor, neighbor_value, temp_assignment
                    ):
                        conflicts += 1

            return conflicts

        return sorted(csp.domains[var], key=lcv_score)

    def copy_domains():
        return {
            var: list(values)
            for var, values in csp.domains.items()
        }

    def forward_check(var, assignment):
        for neighbor in csp.get_neighbors(var):
            if neighbor in assignment:
                continue

            new_domain = []
            for value in csp.domains[neighbor]:
                if csp.is_consistent(neighbor, value, assignment):
                    new_domain.append(value)

            if not new_domain:
                return False

            csp.domains[neighbor] = new_domain

        return True

    def backtrack(assignment):
        if csp.is_complete(assignment):
            return assignment

        var = select_unassigned_variable(assignment)

        for value in order_domain_values(var, assignment):
            if not csp.is_consistent(var, value, assignment):
                continue

            saved_domains = copy_domains()
            csp.assign(var, value, assignment)

            if forward_check(var, assignment):
                result = backtrack(assignment)
                if result is not None:
                    return result

            csp.domains = saved_domains
            csp.unassign(var, assignment)

        return None

    return backtrack({})

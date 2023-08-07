from nltk.sem import logic
from nltk.inference import resolution
from nltk.sem.skolemize import skolemize
from cnfConversion import makeApplications

def getClausesByOrderNum(order, clauseList):
    result = next((x for x in clauseList if x[0] == order), None)
    if result:
        return result
    raise Exception

def shortSolution(solutionFull, originalIndexes):
    result = []
    resolvents = []
    queue = []
    indx, _, parents = solutionFull[-1]
    resolvents.append(indx)
    queue.extend(parents)
    while len(queue) > 0:
        current = queue.pop()
        if current in originalIndexes:
            continue
        resolvents.append(current)
        _, _, parents = getClausesByOrderNum(current, solutionFull)
        queue.extend(parents)

    originalIndexes.sort()
    resolvents.sort()
    for i in originalIndexes:
        result.append(getClausesByOrderNum(i, solutionFull))
    for i in resolvents:
        result.append(getClausesByOrderNum(i, solutionFull))
    return result


def returnFormat(solution):
    result = []
    for order, clauses, parents in solution:
        _clauses = clauses.copy()
        if not len(_clauses):
            result.append((order, '{}', parents))
            continue
        firstExpression = True
        _clause = None
        for expr in _clauses:
            if firstExpression:
                firstExpression = False
                _clause = expr
            else:
                _clause = _clause | expr
        result.append((order, str(_clause), parents))

    return result

def BFS(clauses):
    open = []
    closed = []

    for i, c in enumerate(clauses):
        clauses[i] = (i + 1, c, [i + 1])
    
    open.extend(clauses)

    while len(open) > 0:
        currentOrder, currentClause, _ = open.pop(0)
        closed.append(currentClause)
        if currentClause.is_tautology():
            continue

        for order, clause, _ in clauses:
            resolvents = currentClause.unify(clause)
            if resolvents:
                for r in resolvents:
                    resolvent = (len(clauses) + 1, r, [currentOrder, order])
                    clauses.append(resolvent)
                    if not len(r):
                        return (True, clauses)
                    isInOpen = False
                    for c in [x[1] for x in open]:
                        if c.isSubsetOf(r):
                            isInOpen = True
                            break
                    if isInOpen:
                        break
                    isInClosed = False
                    for c in closed:
                        if c.isSubsetOf(r):
                            isInClosed = True
                    if isInClosed:
                        break
                    open.append(resolvent)
        
    return (False, clauses)
    
def DFS(clauses):
    open = []
    for i, c in enumerate(clauses):
        clauses[i] = (i + 1, c, [i + 1])
    
    open.extend(clauses)

    while len(open) > 0:
        currentOrder, currentClause, _ = open.pop(0)
        if currentClause.is_tautology():
            continue
        for order, clause, _ in clauses:
            resolvents = currentClause.unify(clause)
            if resolvents:
                for r in resolvents:
                    resolvent = (len(clauses) + 1, r, [currentOrder, order])
                    clauses.append(resolvent)
                    if not len(r):
                        return (True, clauses)
                    isInOpen = False
                    for c in [x[1] for x in open]:
                        if c.isSubsetOf(r):
                            isInOpen = True
                            break
                    if isInOpen:
                        break
                    if isInAncestors(clauses, resolvent):
                        break
                    open.insert(0, resolvent)
                    
        
    return (False, clauses)

def getAncestors(clauses, nodeOrder, parents):
    ancestors = []
    _, _, parents = getClausesByOrderNum(nodeOrder, clauses) 

    open = []
    closed = []
    
    open.extend(parents)
    while len(open) > 0:
        currentOrder = open.pop(0)
        ancestors.append(getClausesByOrderNum(currentOrder, clauses)[1])
        closed.append(currentOrder)

        _, _, currentParents = getClausesByOrderNum(currentOrder, clauses)
        if len(currentParents) == 2:
            open.extend(currentParents)
    return ancestors

def isInAncestors(clauses, node):
    order, clause, parents = node
    ancestors = getAncestors(clauses, order, parents)
    
    for a in ancestors:
        if a.isSubsetOf(clause):
            return True
    return False

    


def resolutionMethod(statements, propositional, algorithm):
    logic._counter._value = 0
    clauses = []
    algorithms = {
        'DFS': 0,
        'BFS': 1,
        'NLTK': 2
    }

    for i, s in enumerate(statements):
        expression = logic.Expression.fromstring(s)

        if propositional:
            expression = makeApplications(expression)
        if i == 0:
            expression = expression.negate()

        clause = resolution._clausify(skolemize(expression))
        clauses.extend(clause)

    originalIndexes = list(range(1, len(clauses) + 1))

    try:        
        if algorithms[algorithm] == 0:
            result, clauses = DFS(clauses)
        elif algorithms[algorithm] == 1:
            result, clauses = BFS(clauses)
        elif algorithms[algorithm] == 2:
            result, clauses = resolution.ResolutionProver()._attempt_proof(clauses)

            for i, c in enumerate(clauses):
                if c._parents:
                    firstParent, secondParent = c._parents
                    clauses[i] = (i + 1, c, [firstParent, secondParent])
                else:
                    clauses[i] = (i + 1, c, [i + 1])
        else:
            return False, [], []
        
        if not result:
            full = returnFormat(clauses)
            return False, full, []

        solutionShort = shortSolution(
            clauses.copy(), originalIndexes.copy())

        return True, returnFormat(clauses), returnFormat(solutionShort)

    except Exception as ex:
        return False, [], []

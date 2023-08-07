from nltk.sem import logic
from nltk.inference import resolution
from nltk.internals import Counter
from nltk.sem.skolemize import skolemize, to_cnf

def makeApplications(e):
    argument = logic.IndividualVariableExpression(logic.Variable('x'))

    if isinstance(e, logic.IffExpression):
        first = makeApplications(e.first)
        second = makeApplications(e.second)
        return logic.IffExpression(first, second)
    elif isinstance(e, logic.ImpExpression):
        first = makeApplications(e.first)
        second = makeApplications(e.second)
        return logic.ImpExpression(first, second)
    elif isinstance(e, logic.AndExpression):
        first = makeApplications(e.first)
        second = makeApplications(e.second)
        return logic.AndExpression(first, second)
    elif isinstance(e, logic.OrExpression):
        first = makeApplications(e.first)
        second = makeApplications(e.second)
        return logic.OrExpression(first, second)
    elif isinstance(e, logic.NegatedExpression):
        term = makeApplications(e.term)
        return logic.NegatedExpression(term)
    
    if isinstance(e, logic.FunctionVariableExpression):
        return logic.ApplicationExpression(e, argument)
    elif isinstance(e, logic.ConstantExpression):
        return logic.ApplicationExpression(e, argument)
    elif isinstance(e, logic.BinaryExpression):
        return logic.ApplicationExpression(e, argument)
    elif isinstance(e, logic.BooleanExpression):
        return logic.ApplicationExpression(e, argument)
    elif isinstance(e, logic.TruthValueType):
        return logic.ApplicationExpression(e, argument)
    elif isinstance(e, logic.IndividualVariableExpression):
        return logic.ApplicationExpression(e, argument)
    raise Exception

def removeImplications(expression):
    if isinstance(expression, logic.ImpExpression):
        first = logic.NegatedExpression(removeImplications(expression.first))
        second = removeImplications(expression.second)
        return logic.OrExpression(first, second)
    elif isinstance(expression, logic.IffExpression):
        first = removeImplications(expression.first)
        second = removeImplications(expression.second)
        return logic.AndExpression(first, second)

    if isinstance(expression, logic.AllExpression):
        return logic.AllExpression(variable=expression.variable, term=removeImplications(expression.term))
    elif isinstance(expression, logic.ExistsExpression):
        return logic.ExistsExpression(variable=expression.variable, term=removeImplications(expression.term))
    elif isinstance(expression, logic.AndExpression):
        first = removeImplications(expression.first)
        second = removeImplications(expression.second)
        return logic.AndExpression(first, second)
    elif isinstance(expression, logic.OrExpression):
        first = removeImplications(expression.first)
        second = removeImplications(expression.second)
        return logic.OrExpression(first, second)
    elif isinstance(expression, logic.ApplicationExpression):
        return expression
    elif isinstance(expression, logic.NegatedExpression):
        negated = expression.term

        if isinstance(negated, logic.ImpExpression):
            first = logic.NegatedExpression(removeImplications(negated.first))
            second = removeImplications(negated.second)
            return logic.NegatedExpression(logic.OrExpression(first, second))
        elif isinstance(negated, logic.IffExpression):
            first = removeImplications(negated.first)
            second = removeImplications(negated.second)
            return logic.NegatedExpression(logic.AndExpression(first, second))

        if isinstance(negated, logic.AllExpression):
            return logic.NegatedExpression(logic.AllExpression(variable=negated.variable, term=removeImplications(negated.term)))
        elif isinstance(negated, logic.ExistsExpression):
            return logic.NegatedExpression(logic.ExistsExpression(variable=negated.variable, term=removeImplications(negated.term)))
        elif isinstance(negated, logic.AndExpression):
            first = removeImplications(negated.first)
            second = removeImplications(negated.second)
            return logic.NegatedExpression(logic.AndExpression(first, second))
        elif isinstance(negated, logic.OrExpression):
            first = removeImplications(negated.first)
            second = removeImplications(negated.second)
            return logic.NegatedExpression(logic.OrExpression(first, second))
        elif isinstance(negated, logic.NegatedExpression):
            return logic.NegatedExpression(removeImplications(negated))
        elif isinstance(negated, logic.ApplicationExpression):
            return logic.NegatedExpression(negated)
        raise Exception
    raise Exception

def removeNegations(expression):
    if isinstance(expression, logic.NegatedExpression):
        negated = expression.term
        if isinstance(negated, logic.AllExpression):
            term = removeNegations(negated.term.negate())
            return logic.ExistsExpression(variable=negated.variable, term=term)
        elif isinstance(negated, logic.ExistsExpression):
            term = removeNegations(negated.term.negate())
            return logic.AllExpression(variable=negated.variable, term=term)
        elif isinstance(negated, logic.AndExpression):
            first = removeNegations(negated.first.negate())
            second = removeNegations(negated.second.negate())
            return logic.OrExpression(first, second)
        elif isinstance(negated, logic.OrExpression):
            first = removeNegations(negated.first.negate())
            second = removeNegations(negated.second.negate())
            return logic.AndExpression(first, second)
        elif isinstance(negated, logic.NegatedExpression):
            return removeNegations(negated.negate())
        elif isinstance(negated, logic.ApplicationExpression):
            return negated.negate()
    elif isinstance(expression, logic.AllExpression):
        return logic.AllExpression(variable=expression.variable, term=removeNegations(expression.term))
    elif isinstance(expression, logic.ExistsExpression):
        return logic.ExistsExpression(variable=expression.variable, term=removeNegations(expression.term))
    elif isinstance(expression, logic.AndExpression):
        first = removeNegations(expression.first)
        second = removeNegations(expression.second)
        return logic.AndExpression(first, second)
    elif isinstance(expression, logic.OrExpression):
        first = removeNegations(expression.first)
        second = removeNegations(expression.second)
        return logic.OrExpression(first, second)
    elif isinstance(expression, logic.ApplicationExpression):
        return expression
    raise Exception
    
def makeSkolemized(expression, scope = set(), variables = set()):
    if isinstance(expression, logic.AllExpression):
        term = makeSkolemized(expression.term, scope | {expression.variable}, variables | {expression.variable})
        return term.replace(
            expression.variable,
            logic.VariableExpression(logic.unique_variable(ignore=variables)),
        )
    elif isinstance(expression, logic.ExistsExpression):
        term = makeSkolemized(expression.term, scope, variables | {expression.variable})
        if scope:
            return term.replace(expression.variable, logic.skolem_function(scope))
        else:
            skolem_constant = logic.VariableExpression(logic.unique_variable(ignore=variables))
            return term.replace(expression.variable, skolem_constant)
    elif isinstance(expression, logic.AndExpression):
        first = makeSkolemized(expression.first, scope, variables)
        second = makeSkolemized(expression.second, scope, variables)
        return logic.AndExpression(first, second)
    elif isinstance(expression, logic.OrExpression):
        first = makeSkolemized(expression.first, scope, variables)
        second = makeSkolemized(expression.second, scope, variables)
        return logic.OrExpression(first, second)
    elif isinstance(expression, logic.ApplicationExpression):
        return expression
    elif isinstance(expression, logic.NegatedExpression):
        negated = expression.term
        if isinstance(negated, logic.AllExpression):
            term = makeSkolemized(
                -negated.term, scope, variables | {negated.variable}
            )
            if scope:
                return term.replace(negated.variable, logic.skolem_function(scope))
            else:
                skolem_constant = logic.VariableExpression(
                    logic.unique_variable(ignore=variables)
                )
                return term.replace(negated.variable, skolem_constant)
        elif isinstance(negated, logic.ExistsExpression):
            term = makeSkolemized(
                -negated.term,
                scope | {negated.variable},
                variables | {negated.variable},
            )
            return term.replace(
                negated.variable,
                logic.VariableExpression(logic.unique_variable(ignore=variables)),
            )
        elif isinstance(negated, logic.AndExpression):
            first = makeSkolemized(negated.first, scope, variables)
            second = makeSkolemized(negated.second, scope, variables)
            return logic.AndExpression(first, second)
        elif isinstance(negated, logic.OrExpression):
            first = makeSkolemized(negated.first, scope, variables)
            second = makeSkolemized(negated.second, scope, variables)
            return logic.OrExpression(first, second)
        elif isinstance(negated, logic.ApplicationExpression):
            return negated.negate() #TODO negate?
        elif isinstance(negated, logic.NegatedExpression):
            return makeSkolemized(negated.term, scope, variables).negate()
        raise Exception
    raise Exception

def makeConjuctive(expression):
    if isinstance(expression, logic.OrExpression):
        first = makeConjuctive(expression.first)
        second = makeConjuctive(expression.second)
        return to_cnf(first, second)
    elif isinstance(expression, logic.AndExpression):
        first = makeConjuctive(expression.first)
        second = makeConjuctive(expression.second)
        return logic.AndExpression(first, second)
    elif isinstance(expression, logic.ApplicationExpression):
        return expression
    elif isinstance(expression, logic.NegatedExpression):
        negated = expression.term
        if isinstance(negated, logic.OrExpression):
            first = makeConjuctive(negated.first)
            second = makeConjuctive(negated.second)
            return logic.OrExpression(first, second)
        elif isinstance(negated, logic.AndExpression):
            first = makeConjuctive(negated.first)
            second = makeConjuctive(negated.second)
            return logic.AndExpression(first, second)
        elif isinstance(negated, logic.ApplicationExpression):
            return negated.negate()
        elif isinstance(negated, logic.NegatedExpression):
            return makeConjuctive(negated.term).negate()
        raise Exception
    raise Exception

def convertAll(statements, propositional):
    removedImplications = []
    removedNegations = []
    skolemized = []
    conjuctive = []
    clausified = []
    expressions = []
    goalClausesIndexes = []

    for s in statements:
        _expression = logic.Expression.fromstring(s)
        if propositional:
            _expression = makeApplications(_expression)
        expressions.append(_expression)
    negatedGoal = expressions[0] = expressions[0].negate()

    logic._counter._value = 0

    for e in expressions:
        _removedImplications = removeImplications(e)
        removedImplications.append(_removedImplications)
        
        _removedNegations = removeNegations(_removedImplications)
        removedNegations.append(_removedNegations)
        
        _skolemized = makeSkolemized(_removedNegations)
        skolemized.append(_skolemized)

        _conjuctive = makeConjuctive(_skolemized)
        conjuctive.append(_conjuctive)

        _clausified = resolution._clausify(_conjuctive)
        
        if e == negatedGoal:
            goalClausesIndexes.extend(range(1, len(_clausified) + 1))
        clausified.append(_clausified)

    for i, clauses in enumerate(clausified):
        for j, clause in enumerate(clauses):
            firstExpression = True
            for expr in clause:
                if firstExpression:
                    firstExpression = False
                    clausified[i][j] = expr
                else:
                    clausified[i][j] = clausified[i][j] | expr
            clausified[i][j] = clausified[i][j].simplify()

    return removedImplications, removedNegations, skolemized, conjuctive, clausified, negatedGoal, goalClausesIndexes

from nltk.sem import logic


def validatePropositional(expression):
    if isinstance(
        expression, logic.IffExpression
        ) or isinstance(
        expression, logic.ImpExpression
        ) or isinstance(
        expression, logic.AndExpression
        ) or isinstance(
        expression, logic.OrExpression
        ) or isinstance(
        expression, logic.IffExpression
        ) or isinstance(expression, logic.IffExpression):
        validatePropositional(expression.first)
        validatePropositional(expression.second)
    elif isinstance(expression, logic.NegatedExpression):
        validatePropositional(expression.term)
    elif isinstance(expression, logic.ApplicationExpression):
        raise logic.LogicalExpressionException(-1, "")


def validatePredicate(expression):
    typeCheck = expression.typecheck()
    if len(typeCheck) < 2:
        raise logic.LogicalExpressionException(-1, "")
    for a in typeCheck:
        if isinstance(typeCheck[a], logic.TruthValueType):
            raise logic.LogicalExpressionException(-1, "")


def validate(statement, propositional):
    result = True
    try:
        expr = logic.Expression.fromstring(statement)
        if propositional:
            validatePropositional(expr)
        else:
            validatePredicate(expr)

    except logic.LogicalExpressionException:
        result = False

    return result
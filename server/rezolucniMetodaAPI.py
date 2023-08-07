from flask import Flask, jsonify, request, make_response
import validation
import cnfConversion as cnf
import resolutionMethod as rm

app = Flask(__name__)

def respondToOptions():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    return response

@app.route("/")
def returnMessage():
    response = jsonify(msg="server is up")
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', "*")
    return response


@app.route('/validate', methods=['POST', 'OPTIONS'])
def validate():
    if request.method == "OPTIONS":
        return respondToOptions()
    
    statement = request.json.get('statement')
    propositional = request.json.get('propositional')

    valid = validation.validate(statement=statement, propositional=propositional)

    response = jsonify(valid=valid)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', "*")
    return response

@app.route('/cnf', methods=['OPTIONS', 'POST'])
def cnfConversion():
    if request.method == "OPTIONS":
        return respondToOptions()
    
    statements = request.json.get('statements')
    propositional = request.json.get('propositional')

    removedImplications, removedNegations, skolemized, conjuctive, clausified, negatedGoal, goalIndexes = cnf.convertAll(statements, propositional)

    for i, expression in enumerate(removedImplications):
        removedImplications[i] = str(expression)

    for i, expression in enumerate(removedNegations):
        removedNegations[i] = str(expression)
    
    for i, expression in enumerate(skolemized):
        skolemized[i] = str(expression)

    for i, expression in enumerate(conjuctive):
        conjuctive[i] = str(expression)


    for i, clauses in enumerate(clausified):
        for j, clause in enumerate(clauses):
            clausified[i][j] = str(clause)

    response = jsonify(removedImplications=removedImplications, removedNegations=removedNegations, skolemized=skolemized, conjuctive=conjuctive, clausified=clausified, negatedGoal=str(negatedGoal), goalIndexes=goalIndexes)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', "*")
    return response

@app.route('/solve', methods=['POST', 'OPTIONS'])
def resolutionMethod():
    if request.method == "OPTIONS":
        return respondToOptions()
    
    statements = request.json.get('statements')
    propositional = request.json.get('propositional')
    algorithm = request.json.get('algorithm')
    
    result, full, short = rm.resolutionMethod(statements, propositional, algorithm)

    fullSolution = []
    for order, clause, parents in full:
        obj = {
            "order": str(order),
            "clause": clause,
            "parents": parents
        }
        fullSolution.append(obj)

    shortSolution = []
    for order, clause, parents in short:
        obj = {
            "order": str(order),
            "clause": clause,
            "parents": parents
        }
        shortSolution.append(obj)

    response = jsonify(result=result, fullSolution=fullSolution, shortSolution=shortSolution)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', "*")
    return response
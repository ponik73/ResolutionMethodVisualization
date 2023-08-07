import { LogicSymbols, statementList, type StatementListObject } from "./statement";
import { logicDomain, DomainType, isPropositional, usedAlgorithm } from "./domain";
import { SERVER_ERROR_MSG } from "./helper";
import axios from "axios";
import { ref } from "vue";
import { ElMessage } from "element-plus";

function stringRepresentStatementList(): string[] {
    const _statementList: string[] = [];
    statementList.value.forEach(_statement => {
        _statementList.push(_statement.statement);
    });
    return _statementList
}

function removeApplications(negatedGoal: string, removedImplications: string[], skolemized: string[], clausified: string[][], removedNegations: string[], conjuctive: string[], solution: SolutionNode[] = []): string {
    const _var = '(x)'

    negatedGoal = negatedGoal.split(_var).join('')

    removedImplications.forEach((_statement, index) => {
        removedImplications[index] = _statement.split(_var).join('');
    });

    skolemized.forEach((_statement, index) => {
        skolemized[index] = _statement.split(_var).join('');
    });

    clausified.forEach((_clauses, i) => {
        _clauses.forEach((_clause, j) => {
            clausified[i][j] = _clause.split(_var).join('');
        })
    });

    solution.forEach((_node, index) => {
        solution[index].clause = _node.clause.split(_var).join('');
    });

    removedNegations.forEach((_statement, index) => {
        removedNegations[index] = _statement.split(_var).join('');
    });

    conjuctive.forEach((_statement, index) => {
        conjuctive[index] = _statement.split(_var).join('');
    });

    return negatedGoal
}

export const goalClausesIndexes = ref<number[]>([]);

interface ConversionResponse {
    clausified: string[][],
    removedImplications: string[],
    skolemized: string[],
    negatedGoal: string,
    goalClauses: number[],
    removedNegations: string[],
    conjuctive: string[]
};

export async function convertToCnf(): Promise<ConversionResponse> {
    const result: ConversionResponse = { clausified: [], removedImplications: [], skolemized: [], negatedGoal: '', goalClauses: [], conjuctive: [], removedNegations: [] };

    try {
        const response = await axios.post(import.meta.env.VITE_CNF_ROUTE, { statements: stringRepresentStatementList(), propositional: isPropositional() });

        result.removedImplications = response.data.removedImplications;
        result.clausified = response.data.clausified;
        result.skolemized = response.data.skolemized;
        result.negatedGoal = response.data.negatedGoal;
        result.goalClauses = response.data.goalIndexes;
        result.removedNegations = response.data.removedNegations;
        result.conjuctive = response.data.conjuctive;

        if (isPropositional())
            result.negatedGoal = removeApplications(result.negatedGoal, result.removedImplications, result.skolemized, result.clausified, result.removedNegations, result.conjuctive);

        goalClausesIndexes.value = [...result.goalClauses];

        return result;
    } catch (error) {
        ElMessage({
            message: SERVER_ERROR_MSG,
            type: 'error',
        })
        return result;
    }
}

export function setPages(cnfData: ConversionResponse) {
    const removedImplications: StatementListObject[] = [];
    const skolemized: StatementListObject[] = [];
    const clausified: StatementListObject[] = [];
    const removedNegations: StatementListObject[] = [];
    const conjuctive: StatementListObject[] = [];

    cnfData.removedImplications.forEach(_statement => {
        removedImplications.push({ order: removedImplications.length + 1, statement: _statement.split('.').join('') })
    });

    cnfData.skolemized.forEach(_statement => {
        skolemized.push({ order: skolemized.length + 1, statement: _statement })
    });

    cnfData.clausified.forEach(clauses => {
        clauses.forEach(clause => {
            clausified.push({ order: clausified.length + 1, statement: clause })
        })
    });

    cnfData.removedNegations.forEach(_statement => {
        removedNegations.push({ order: removedNegations.length + 1, statement: _statement })
    });

    cnfData.conjuctive.forEach(_statement => {
        conjuctive.push({ order: conjuctive.length + 1, statement: _statement })
    });

    const pages =  [
        {
            heading: `Pôvodné výroky (${logicDomain.value.toLowerCase()})`,
            statements: statementList.value,
            wikiId: 'clausularFormConversion',
        },
        {
            heading: 'Odstránenie implikácií a negácia záveru',
            statements: removedImplications,
            wikiId: 'cnfRemoveImplications',
        },
        {
            heading: 'Odstránenie negácií',
            statements: removedNegations,
            wikiId: 'cnfRemoveNegations',
        },
        {
            heading: 'Skolemizácia a odstránenie univerzálnych kvantifikátorov',
            statements: skolemized,
            wikiId: 'cnfSkolemize',
        },
        {
            heading: 'Konjunktívna normálna forma',
            statements: conjuctive,
            wikiId: 'cnfCnf',
        },
        {
            heading: 'Klauzulárna forma',
            statements: clausified,
            wikiId: 'cnfFinish'
        }
    ];

    if(isPropositional())
        return pages.filter(page => {
            return page.wikiId != 'cnfSkolemize';
        })
    return pages;
}

export interface SolutionNode {
    order: number,
    clause: string,
    parents: number[],
}
interface SolveResponse {
    result: boolean,
    fullSolution: SolutionNode[],
    shortSolution: SolutionNode[],
}

export const resolutionResult = ref<boolean>(false);
export const solutionFull = ref<SolutionNode[]>([]);
export const solutionShort = ref<SolutionNode[]>([]);

export async function solve() {
    const solved: SolveResponse = { result: false, fullSolution: [], shortSolution: [] };
    solutionFull.value.length = 0;
    solutionShort.value.length = 0;

    try {
        const response = await axios.post(import.meta.env.VITE_SOLVE_ROUTE, { statements: stringRepresentStatementList(), propositional: isPropositional(), algorithm: usedAlgorithm.value })

        solved.result = response.data.result;
        solved.fullSolution = response.data.fullSolution;
        solved.shortSolution = response.data.shortSolution;

        if (isPropositional()) {
            removeApplications('', [], [], [], [], [], solved.fullSolution);
            if (solved.result)
                removeApplications('', [], [], [], [], [], solved.shortSolution);
        }

        resolutionResult.value = solved.result;
        solved.fullSolution.forEach(node => {
            const _order = solutionFull.value.length + 1;
            const _clause: string[] = [];
            if (node.clause === '{}')
                _clause.push('\u2610');
            else
                _clause.push(node.clause);
            _clause[0] = _clause[0].split('|').join(LogicSymbols.OR)
            _clause[0] = _clause[0].split('-').join(LogicSymbols.NOT)
            solutionFull.value.push({ order: _order, clause: _clause[0], parents: node.parents })
        })

        if (!solved.result)
            return
        const fullVsShortIndxs: [number, number][] = [];
        solved.shortSolution.forEach(node => {
            const _order = solutionShort.value.length + 1;
            fullVsShortIndxs.push([+ node.order, _order])
            const _clause: string[] = [];
            if (node.clause === '{}')
                _clause.push('\u2610');
            else
                _clause.push(node.clause);
            const _parents: number[] = [];

            node.parents.forEach((parentIndex) => {
                fullVsShortIndxs.forEach((map) => {
                    if (map[0] === parentIndex) {
                        _parents.push(map[1]);
                    }
                });
            });
            solutionShort.value.push({ order: _order, clause: _clause[0], parents: _parents })
        });

    } catch (error) {
        console.log(error);
        ElMessage({
            message: SERVER_ERROR_MSG,
            type: 'error',
        })
    }
}

export function getClauseByOrder(order: number, shorten: boolean = false) {
    if (shorten) {
        const clause = solutionShort.value.find((node) => {
            return node.order === order
        });

        return clause ? clause.clause : '';
    }
    const clause = solutionFull.value.find((node) => {
        return node.order === order
    });

    return clause ? clause.clause : '';
}

export function createGraph() {
    
}
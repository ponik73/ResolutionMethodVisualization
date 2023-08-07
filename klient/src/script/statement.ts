import { ref, watch } from 'vue';
import { logicDomain, DomainType, isPropositional } from './domain'
import { SERVER_ERROR_MSG } from './helper';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export interface StatementListObject {
    order: number,
    statement: string
}
export const statementList = ref<StatementListObject[]>([]);
export const conclusionIndex = ref(-1);


watch(logicDomain, () => {
    statementList.value.length = 0;
})

export enum LogicSymbols {
    FORALL = '∀',
    EXISTS = '∃',
    NOT = '¬',
    AND = '∧',
    OR = '∨',
    IF = '⇒',
    IFF = '⇔'
}

export function getNLTKSymbol(sym: LogicSymbols): string {
    switch (sym) {
        case LogicSymbols.FORALL:
            return 'all';
        case LogicSymbols.EXISTS:
            return 'exists';
        case LogicSymbols.NOT:
            return '-';
        case LogicSymbols.AND:
            return '&';
        case LogicSymbols.OR:
            return '|';
        case LogicSymbols.IF:
            return '->';
        case LogicSymbols.IFF:
            return '<->';
    };
}

export function getAvailableSymbols() {
    const availableSymbols: LogicSymbols[] = [];

    switch (logicDomain.value) {
        case DomainType.PREDICATE_LOGIC:
            availableSymbols.push(LogicSymbols.FORALL, LogicSymbols.EXISTS);
        case DomainType.PROPOSITIONAL_LOGIC:
            availableSymbols.push(LogicSymbols.NOT, LogicSymbols.AND, LogicSymbols.OR, LogicSymbols.IF, LogicSymbols.IFF)
            break;
        default:
            availableSymbols.length = 0;
            break;
    };

    return availableSymbols;
}

function checkCharacters(statement: string): boolean {
    const validCharacters = ['(', ')'];

    switch (logicDomain.value) {
        case DomainType.PREDICATE_LOGIC:
            validCharacters.push(getNLTKSymbol(LogicSymbols.FORALL), getNLTKSymbol(LogicSymbols.EXISTS));
            validCharacters.push('a-z');
        case DomainType.PROPOSITIONAL_LOGIC:
            validCharacters.push(getNLTKSymbol(LogicSymbols.NOT), getNLTKSymbol(LogicSymbols.AND), getNLTKSymbol(LogicSymbols.OR), getNLTKSymbol(LogicSymbols.IF), getNLTKSymbol(LogicSymbols.IFF));
            validCharacters.push('A-Z');
            break;
        default:
            validCharacters.length = 0;
            break;
    }
    
    const _statement = statement.replace(/\s/g, "");

    const match = _statement.match(new RegExp(`[${validCharacters}]+`));

    return !!match && match.join('') === _statement;
}

async function validateNLTK(statement: string): Promise<boolean> {
    try {
        const NLTKValidatorResponse = await axios.post(import.meta.env.VITE_VALIDATE_URL, { statement: statement, propositional: isPropositional() }, undefined);

        return NLTKValidatorResponse.data.valid;
    } catch (error) {
        ElMessage({message: SERVER_ERROR_MSG,
            type: 'error',})
        return false;
    }
}


export interface ValidationResponse {
    valid: boolean,
    errorMessage: string
}
export async function validateNewStatement(statement: string, response: ValidationResponse) {
    const ERROR_MESSAGE = 'Nevalidný výrok';

    response.valid = checkCharacters(statement);

    if (!response.valid) {
        response.errorMessage = ERROR_MESSAGE;
        return;
    }

    response.valid = await validateNLTK(statement);

    if (response.valid)
        return;

    response.errorMessage = ERROR_MESSAGE;
}

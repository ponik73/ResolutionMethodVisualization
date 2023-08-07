import { ref } from "vue";
import { LogicSymbols } from '@/script/statement'
import { statementList, conclusionIndex, type StatementListObject } from "@/script/statement";
import type { Router } from "vue-router";
import { resolutionResult, solutionFull, solutionShort } from "./resolution";

export function convertStatementFromNLTKFormat(statement: string): string {
    let result = statement;

    result = result.split('.').join('');

    result = result.split('all ').join(` ${LogicSymbols.FORALL} `);

    result = result.replace('exists', LogicSymbols.EXISTS);
    result = result.split('exists ').join(` ${LogicSymbols.EXISTS }`);

    result = result.split('->').join(LogicSymbols.IF);

    result = result.split('<->').join(LogicSymbols.IFF);

    result = result.split('-').join(LogicSymbols.NOT);

    result = result.split('&').join(LogicSymbols.AND);

    result = result.split('|').join(LogicSymbols.OR);

    return result;
}

export function reorderStatements() {
    const result: StatementListObject[] = []
    const goal = statementList.value.find((_statement) => _statement.order === conclusionIndex.value);
    if (goal) {
        result.push({ order: goal.order, statement: goal.statement })
        result[0].order = 1;
    }

    statementList.value.forEach(_statement => {
        if (_statement.order != conclusionIndex.value)
            result.push({ order: result.length + 1, statement: _statement.statement });
    });

    statementList.value.length = 0
    conclusionIndex.value = 1;

    result.forEach(_element => {
        statementList.value.push(_element);
    });
}

export const SERVER_ERROR_MSG = 'Chyba na strane servera';

export function fromScratch(router: Router) {
    statementList.value.length = 0
    conclusionIndex.value = -1;

    resolutionResult.value = false;
    solutionFull.value.length = 0;
    solutionShort.value.length = 0;

    router.push({ name: 'home' });
}

export function redirectWiki(router: Router) {
    router.push({ name: 'wikiMain' });
}

export function redirectWikiSection(router: Router, section: string) {
    router.push({ name: 'wikiMain', hash: `#${section}` });
}

export const appHeading = ref('Rezolučná metóda');

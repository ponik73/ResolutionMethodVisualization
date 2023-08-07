export enum DomainType{
    PROPOSITIONAL_LOGIC = 'Výroková logika',
    PREDICATE_LOGIC = 'Predikátová logika'
}

export enum Algorithm{
    BFS = 'BFS',
    DFS = 'DFS',
    NLTK = 'NLTK'
}

import { ref } from "vue";
export const logicDomain = ref<DomainType>(DomainType.PREDICATE_LOGIC);
export const usedAlgorithm = ref<Algorithm>(Algorithm.DFS);

export function isPropositional(): boolean {
    return logicDomain.value === DomainType.PROPOSITIONAL_LOGIC;
}

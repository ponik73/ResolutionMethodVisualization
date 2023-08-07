<template>
    <div id="viewContainer">
        <ElContainer id="viewContent">
            <ElAside id="asideContainer">
                <div class="controlContainer">
                    <TextInfo :text="'Rezolúcia'" :wiki-id="'resolution'" />
                    <span class="controlButtonContainer" v-if="resolutionResult" @click="showShorten = !showShorten">
                        <ElButton type="primary">
                            <span v-if="!showShorten">Skrátený dôkaz</span>
                            <span v-else>Úplný dôkaz</span>
                        </ElButton>
                    </span>
                    <span class="controlButtonContainer" @click="ROUTER.push({ name: 'graph' })">
                        <ElButton type="primary">
                            Graf stavového priestoru
                        </ElButton>
                    </span>
                    <span class="controlButtonContainer" @click="fromScratch(ROUTER)">
                        <ElButton type="warning">Nový výpočet</ElButton>
                    </span>
                </div>
            </ElAside>
            <ElMain id="mainContainer">
                <div id="result">
                    <span>Klauzuly</span>
                    <div>
                        <span>Tvrdenie</span>
                        <span v-if="statementList.length > 0" style="font-weight: bolder;">{{
                            statementList[0].statement
                        }}</span>
                        <span v-if="resolutionResult" style="color: var(--el-color-success-dark-2);">je
                            pravdivé</span>
                        <span v-else style="color: var(--el-color-danger-dark-2);">je nepravdivé</span>
                    </div>
                </div>
                <Clause v-for="item in clauses" :id="`clause${item.order}`" :order="item.order" :clause="item.clause"
                    :parents="item.parents" :first-parent-clause="''" :second-parent-clause="''" />
                <span>Rezolventy</span>
                <TransitionGroup tag="div" class="transition" name="fade">
                    <div key="all" v-if="!showShorten">
                        <Clause v-for="item in resolvents" :key="item.order" :id="`clause${item.order}`" :order="item.order"
                            :clause="item.clause" :parents="item.parents" @scroll-to-clause="scrollToClause"
                            @highlight-parents="highlightParents" :first-parent-clause="getClauseByOrder(item.parents[0])"
                            :second-parent-clause="getClauseByOrder(item.parents[1])" />
                    </div>
                    <div key="shorten" v-else>
                        <Clause v-for="item in resolventsShort" :key="item.order" :id="`clause${item.order}Shorten`"
                            :order="item.order" :clause="item.clause" :parents="item.parents"
                            @scroll-to-clause="scrollToClause" @highlight-parents="highlightParents"
                            :first-parent-clause="getClauseByOrder(item.parents[0], true)"
                            :second-parent-clause="getClauseByOrder(item.parents[1], true)" />
                    </div>
                </TransitionGroup>
            </ElMain>
        </ElContainer>
    </div>
</template>

<script setup lang="ts">
import Clause from '@/components/Clause.vue';
import TextInfo from '@/components/TextInfo.vue';
import { usedAlgorithm } from '@/script/domain';
import { reorderStatements, fromScratch, appHeading } from '@/script/helper';
import { solutionFull, solve, resolutionResult, getClauseByOrder, type SolutionNode, solutionShort } from '@/script/resolution';
import { statementList } from '@/script/statement';
import { ElAside, ElButton, ElContainer, ElLoading, ElMain } from 'element-plus';
import { nextTick, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const ROUTER = useRouter();

const clauses = ref<SolutionNode[]>([]);
const resolvents = ref<SolutionNode[]>([]);
const resolventsShort = ref<SolutionNode[]>([]);
const showShorten = ref(false);

function scrollToClause(order: number) {
    let id = `clause${order}${showShorten.value ? 'Shorten' : ''}`;
    clauses.value.forEach(node => {
        if (node.order === order)
            id = `clause${order}`;
    })
    const div = document.getElementById(id);
    if (div) {
        div.scrollIntoView({ behavior: 'smooth', block: 'center' });
        div.style.border = '1px solid var(--el-color-warning)';
        setTimeout(stopHighlight, 1000, div);
        function stopHighlight(div: any) {
            div.style.border = '';
        }
    }
}

function highlightParents(firstParent: number, secondParent: number, start: boolean = true) {
    let id = `clause${firstParent}${showShorten.value ? 'Shorten' : ''}`;
    clauses.value.forEach(node => {
        if (node.order === firstParent)
            id = `clause${firstParent}`;
    })
    const firstParentDiv = document.getElementById(id);

    id = `clause${secondParent}${showShorten.value ? 'Shorten' : ''}`;
    clauses.value.forEach(node => {
        if (node.order === secondParent)
            id = `clause${secondParent}`;
    })
    const secondParentDiv = document.getElementById(id);

    if (firstParentDiv) {
        if (start)
            firstParentDiv.style.border = '1px solid var(--el-color-warning)';
        else
            firstParentDiv.style.border = '';
    }

    if (secondParentDiv) {
        if (start)
            secondParentDiv.style.border = '1px solid var(--el-color-warning)';
        else
            secondParentDiv.style.border = '';
    }

}

onMounted(async () => {
    if (statementList.value.length < 2) {
        ROUTER.replace({ name: 'home' });
        return;
    }
    
    appHeading.value = `Rezolúcia (algoritmus ${usedAlgorithm.value})`;

    if (solutionFull.value.length < 1) {

        reorderStatements();
        const loadingInstance = ElLoading.service({ fullscreen: true })
        await solve();
        nextTick(() => {
            loadingInstance.close()
        })
    }
    const _clauses = solutionFull.value.filter(node => {
        return node.parents.length === 1
    })
    _clauses.forEach(node => {
        clauses.value.push(node)
    });

    const _resolvents = solutionFull.value.filter(node => {
        return node.parents.length === 2
    })
    _resolvents.forEach(node => {
        resolvents.value.push(node)
    });

    if (resolutionResult.value) {
        const _resolventsShort = solutionShort.value.filter(node => {
            return node.parents.length === 2
        });
        _resolventsShort.forEach(node => {
            resolventsShort.value.push(node);
        })
    };
})
</script>

<style scoped>
#viewContainer {
    width: 100%;
    max-width: var(--max-width);
    height: 100%;
    max-height: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#viewHeadline {
    padding-top: 30px;
    line-height: normal;
    font-size: 1.5rem;
}

#viewContent {
    width: 100%;
    max-height: 100%;
}

#asideContainer {
    width: fit-content;
    display: flex;
    align-items: center;
    position: sticky;
}

#mainContainer {
    overflow: scroll;
    max-height: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.transition {
    position: relative;
    padding: 0;
}

.fade-move,
.fade-enter-active,
.fade-leave-active {
    transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: scaleY(0.01) translate(30px, 0);
}

.fade-leave-active {
    position: absolute;
}

#result {
    display: flex;
    justify-content: space-between;
}

#result div {
    display: flex;
    gap: 10px;
}

#stateSpaceGraph {
    width: 800px;
    height: 400px;
    border: 1px solid lightgray;
}
</style>
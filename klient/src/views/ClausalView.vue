<template>
    <div id="viewContainer">
        <ElContainer id="viewContent">
            <ElAside id="asideContainer">
                <div class="controlContainer">
                    <TextInfo :text="'Klauzulárna forma'" :wiki-id="'clausularForm'"/>
                    <span class="controlButtonContainer" @click="showSolution">
                        <ElButton type="warning">Nasledujúci krok</ElButton>
                    </span>
                </div>
            </ElAside>
            <ElMain id="mainContainer">
                <div id="detailedContent">
                    <ElCarousel height="95%" :autoplay="false" arrow="always" trigger="click">
                        <ElCarouselItem v-for="item, i in pages.slice(1)" :key="item.heading">
                            <div class="content">
                                <div class="contentHeading">
                                    <span>{{ i + 1 }}:</span>
                                    <TextInfo :text="item.heading" :wiki-id="item.wikiId"/>
                                </div>
                                <div class="contentStatements">
                                    <div v-if="item.heading === pages[pages.length - 1].heading">
                                        <Clause v-for="statement in item.statements" :order="statement.order"
                                        :clause="statement.statement" :parents="[]" :first-parent-clause="''"
                                        :second-parent-clause="''"></Clause>
                                    </div>
                                    <div v-for="statement in item.statements" :key="statement.order" class="conversion" v-else>
                                        <Statement :order="statement.order" :statement="getStatementByOrder(statement.order, i)" :editable="false"/>
                                        <span style="align-self: center;"><ElIcon><Bottom/></ElIcon></span>
                                        <Statement :order="statement.order" :statement="getStatementByOrder(statement.order, i + 1)" :editable="false"/>
                                    </div>
                                    
                                </div>
                            </div>
                        </ElCarouselItem>
                    </ElCarousel>

                </div>
            </ElMain>
        </ElContainer>
    </div>
</template>

<script setup lang="ts">
import Clause from '@/components/Clause.vue';
import Statement from '@/components/Statement.vue';
import TextInfo from '@/components/TextInfo.vue';
import { reorderStatements, appHeading } from '@/script/helper';
import { ElAside, ElButton, ElCarousel, ElCarouselItem, ElContainer, ElIcon, ElLoading, ElMain } from 'element-plus';
import { nextTick, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { statementList, type StatementListObject } from '@/script/statement';
import { convertToCnf, setPages } from '@/script/resolution';
import { Bottom } from '@element-plus/icons-vue';

const ROUTER = useRouter();

interface Page {
    heading: string,
    statements: StatementListObject[],
    wikiId: string
}
const pages = ref<Page[]>([]);

function showSolution() {
    ROUTER.push({ name: 'solution' });
}

function getStatementByOrder(order: number, pageId: number) {
    const result = pages.value[pageId].statements.find(s => s.order === order);
    if (result) {
        return result.statement;
    }
    return '';
}

onMounted(async () => {
    if (statementList.value.length < 2) {
        ROUTER.replace({ name: 'home' });
        return;
    }
    appHeading.value = 'Prevod výrokov do klauzulárnej formy';
    reorderStatements();
    const loadingInstance = ElLoading.service({ fullscreen: true })
    const cnf = await convertToCnf();
    nextTick(() => {
        loadingInstance.close()
    })
    pages.value = setPages(cnf);
});
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
    padding-block: 30px;
}

#viewContent {
    width: 100%;
}

#asideContainer {
    width: fit-content;
    display: flex;
    align-items: center;
}

#detailedContent {
    width: 100%;
    height: 100%;
    max-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.content {
    padding-inline: calc(16px + var(--el-carousel-arrow-size) + 5px);
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
    overflow: scroll;
}

.contentHeading {
    align-self: center;
    display: flex;
    gap: 10px;
}

.contentStatements {
    height: 100%;
    overflow: scroll;
}

#statementSection,
#cnfSection {
    flex-grow: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    height: 100%;
}

.slide-up-enter-active,
.slide-up-leave-active {
    transition: all 0.3s ease-out;
}

.slide-up-enter-from {
    opacity: 0;
    transform: translateY(100%);
}

.slide-up-leave-to {
    opacity: 0;
    transform: translateY(-100%);
}

#detailedContent .el-carousel.el-carousel--horizontal {

    width: 100%;
    height: 100%;
    --el-carousel-arrow-background: #393a3c;
    --el-carousel-arrow-hover-background: #a6a9ad;
}

.conversion {
    display: flex;
    flex-direction: column;
}
</style>
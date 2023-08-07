<template>
    <div class="clauseContainer" :class="{ conclusion: isConclusionClause, assumption: isAssumption }">
        <div class="content">
            <span class="order">{{ order }}</span>
            <span class="clause">{{ convertStatementFromNLTKFormat(clause) }}</span>
        </div>
        <div class="parents" v-if="!isAssumption">
            <ElTooltip placement="left">
                <template #content>
                    <span style="font-size: medium;">
                        {{ convertStatementFromNLTKFormat(firstParentClause) }}
                        <br />
                        {{ convertStatementFromNLTKFormat(secondParentClause) }}
                    </span>
                </template>
                <div @mouseenter="$emit('highlightParents', parents[0], parents[1])"
                    @mouseleave="$emit('highlightParents', parents[0], parents[1], false)">
                    <span>[</span>
                    <span class="parent" @click="$emit('scrollToClause', parents[0])">{{ parents[0] }}</span>
                    <span>, </span>
                    <span class="parent" @click="$emit('scrollToClause', parents[1])">{{ parents[1] }}</span>
                    <span>]</span>
                </div>
            </ElTooltip>
        </div>
    </div>
</template>

<script setup lang="ts">
import { goalClausesIndexes } from '@/script/resolution';
import type { ElTooltip } from 'element-plus';
import { ref } from 'vue';
import { convertStatementFromNLTKFormat } from '@/script/helper'

const PROPS = defineProps<{
    order: number,
    clause: string,
    parents: number[],
    firstParentClause: string,
    secondParentClause: string,
}>();
const EMITS = defineEmits(['scrollToClause', 'highlightParents']);

const isConclusionClause = ref(false);
const isAssumption = ref(false)
if (goalClausesIndexes.value.includes(PROPS.order))
    isConclusionClause.value = true

if (PROPS.parents.length < 2)
    isAssumption.value = true
</script>

<style scoped>
.clauseContainer {
    margin-block: 5px;
    display: flex;
    background-color: var(--el-color-primary-light-7);
    padding: 8px;
    border-radius: 5px;
    font-size: larger;
    align-items: center;
    justify-content: space-between;
}

.content {
    display: flex;
    align-items: center;
    gap: 20px;
}

.clauseContainer:first-child {
    margin-top: 0;
}

.clauseContainer:last-child {
    margin-bottom: 0;
}

.order::after {
    content: ')';
}

.clauseContainer.assumption {
    background-color: #636466;
}

.clauseContainer.conclusion.assumption {
    background-color: var(--el-color-success-light-5);
}

.parent:hover {
    cursor: pointer;
    color: var(--el-color-warning);
    text-decoration: underline 1px var(--el-color-warning);
}
</style>
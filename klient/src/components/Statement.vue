<template>
    <div class="statementContainer" :class="{ conclusion: isConclusionStatement, notEditable: !editable }">
        <div class="content">
            <span class="order">{{ order }}</span>
            <span class="statement">{{ convertStatementFromNLTKFormat(statement) }}</span>
        </div>
        <div class="controls" v-if="editable">
            <ElButton type="primary" :icon="Edit" circle @click="$emit('editStatement')"/>
            <ElButton type="danger" :icon="Delete" circle @click="$emit('deleteStatement')" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { conclusionIndex } from '@/script/statement';
import { Delete, Edit } from '@element-plus/icons-vue';
import { computed } from '@vue/reactivity';
import { ElButton } from 'element-plus';
import { convertStatementFromNLTKFormat } from '@/script/helper'

const PROPS = defineProps<{
    order: number,
    statement: string,
    editable: boolean
}>();

const EMITS = defineEmits(['deleteStatement', 'editStatement']);

const isConclusionStatement = computed(() => { return PROPS.order === conclusionIndex.value });

</script>

<style scoped>
.statementContainer {
    margin-block: 5px;
    display: flex;
    gap: 50px;
    background-color: #636466;
    padding: 5px;
    border-radius: 5px;
    font-size: larger;
    align-items: center;
    justify-content: space-between;
}

.statementContainer:first-child {
    margin-top: 0;
}

.statementContainer:last-child {
    margin-bottom: 0;
}

.content {
    display: flex;
    align-items: center;
    gap: 20px;
}

.controls {
    display: flex;
}

.order,
.statement {
    color: var(--el-text-color-primary);
}

.order::after {
    content: ')';
}

.statementContainer.conclusion {
    background-color: var(--el-color-success-light-5);
}

.statementContainer.notEditable {
    padding: 8px;
    margin-block: 5px;
}
</style>
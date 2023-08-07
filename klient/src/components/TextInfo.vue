<template>
    <div class="TextInfoContainer">
        <span>{{ text }}</span>
        <ElIcon color="var(--el-color-primary)" @click="redirectWikiSection(ROUTER, wikiId)"> 
            <InfoFilled />
        </ElIcon>
    </div>
</template>

<script setup lang="ts">
import { ElIcon } from 'element-plus';
import { InfoFilled } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';
import {redirectWikiSection } from '@/script/helper'

defineProps<{
  text: string,
  wikiId: string
}>()

const ROUTER = useRouter();
</script>

<style  scoped>
.TextInfoContainer {
    display: flex;
    flex-direction: row;
    gap: 20px;
    width: fit-content;
    align-items: center;
    justify-content: center;
}

.TextInfoContainer span{
    color: var(--el-text-color-regular);
}

.TextInfoContainer .el-icon:hover{
    cursor: pointer;
}
</style>
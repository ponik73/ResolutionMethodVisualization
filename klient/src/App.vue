<script setup lang="ts">
import { ElLink } from 'element-plus';
import { RouterView, useRouter } from 'vue-router';
import { appHeading, redirectWiki, fromScratch } from '@/script/helper'
import router from './router';

const ROUTER = useRouter();

</script>

<template>
  <div class="appHeader">
    <h1>{{ appHeading }}</h1>
    <div class="appHeaderLinks">
    <ElLink @click="fromScratch(router)" :disabled="ROUTER.currentRoute.value.name === 'home'">Domov</ElLink>
    <ElLink @click="redirectWiki(router)" :disabled="ROUTER.currentRoute.value.name === 'wikiMain'">Wiki</ElLink>
  </div>
</div>
  <RouterView v-slot="{ Component }" class="appView">
    <Transition class="transition" name="fade">
      <Component :is="Component"/>
    </Transition>
  </RouterView>
</template>

<style scoped>
.appHeader {
  padding-top: 10px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  max-width: var(--max-width);
  border-bottom: 1px solid var(--el-text-color-regular);
}

.appHeaderLinks{
  display: flex;
  gap: 20px;
  height: fit-content;
}

.appView{
  height: 100%;
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
</style>
<script setup lang="ts">
import { ElIcon, ElLink, ElSelect } from 'element-plus';
import TextInfo from '../components/TextInfo.vue';
import { CircleCheckFilled } from '@element-plus/icons-vue';
import { Algorithm, DomainType, logicDomain, usedAlgorithm } from '../script/domain'
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { appHeading, redirectWikiSection } from '@/script/helper';

const domainOptions = [
  {
    value: DomainType.PROPOSITIONAL_LOGIC,
    label: DomainType.PROPOSITIONAL_LOGIC,
  },
  {
    value: DomainType.PREDICATE_LOGIC,
    label: DomainType.PREDICATE_LOGIC,
  }
]

const algorithmOptions = [
  {
    value: Algorithm.DFS,
    label: 'Prehľadávanie do hĺbky (DFS) [odporúčané]'
  },
  {
    value: Algorithm.BFS,
    label: 'Prehľadávanie do šírky (BFS)'
  },
  {
    value: Algorithm.NLTK,
    label: 'Algoritmus knižnice NLTK'
  }
]

const ROUTER = useRouter();

onMounted(() => {
  appHeading.value = 'Rezolučná metóda';
})

function redirectStamentsInput() {
  ROUTER.push({ name: 'statementsInput' });
}

</script>

<template>
  <div class="mainContainer">
    <div class="contentContainer">
      <div id="infoSection">
        <ElLink class="linkBiggerText" @click="redirectWikiSection(ROUTER, 'resolutionMethod')">
          Informácie o rezolučnej metóde
        </ElLink>
        <ElLink class="linkBiggerText" @click="redirectWikiSection(ROUTER, 'about')">O stránke</ElLink>
      </div>
      <div id="subheading">
        <h2>Zadanie parametrov</h2>
      </div>
      <div id="domainSection">
        <div class="selection">
          <span>Doména</span>
          <ElSelect v-model="logicDomain" class="m-2" placeholder="Select" size="large">
            <el-option v-for="item in domainOptions" :key="item.value" :label="item.label" :value="item.value" />
          </ElSelect>
        </div>
        <div class="selection">
          <TextInfo :text="'Algoritmus:'" :wiki-id="'searchAlgoritm'" />
          <ElSelect v-model="usedAlgorithm" class="m-2" placeholder="Select" size="large">
            <el-option v-for="item in algorithmOptions" :key="item.value" :label="item.label" :value="item.value" />
          </ElSelect>
        </div>
        <ElIcon :size="50" color="var(--el-color-primary)" @click="redirectStamentsInput">
          <CircleCheckFilled />
        </ElIcon>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mainContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: inherit;
  width: 100%;
  padding-block: 20px;
  max-height: 100%;
  height: 100%;
}

.mainHeadline {
  padding-block: 30px;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  text-align: center;
}

.contentContainer {
  padding-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

#infoSection {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

#domainSection {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.selection {
  display: flex;
  flex-direction: column;
  gap: 5px;
  align-items: flex-start;
}

.linkBiggerText {
  font-size: var(--el-font-size-medium);
}
</style>

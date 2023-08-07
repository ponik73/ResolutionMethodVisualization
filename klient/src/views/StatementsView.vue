<template>
  <div id="viewContainer">
    <el-container id="viewContent">
      <el-aside id="asideContainer">
        <div class="controlContainer">
          <span class="controlButtonContainer" @click="exampleDialogVisible = true;">
            <ElButton type="primary">Príklady</ElButton>
          </span>
          <span class="controlButtonContainer" @click="ROUTER.replace({ name: 'home' })">
            <ElButton type="primary">Zmena parametrov</ElButton>
          </span>
          <span class="controlButtonContainer"
            @click="() => { statementInputDialogVisible = true; inputDialogTitle = 'Nový výrok'; editStatementOrder = -1 }">
            <ElButton type="primary">Pridať výrok</ElButton>
          </span>
          <span class="controlButtonContainer" @click="nextStep">
            <ElButton type="warning">Nasledujúci krok</ElButton>
          </span>
        </div>
      </el-aside>
      <el-main id="mainContainer">
        <div id="mainContent">
          <TextInfo :text="'Výroky:'" :wiki-id="''"/>
          <div id="statements">
            <Statement v-for="obj in statementList" :order="obj.order" :statement="obj.statement" editable
              @delete-statement="deleteStatement(obj.order)" @edit-statement="editStatement(obj.order)" />
          </div>
        </div>
      </el-main>
    </el-container>

    <ElDialog v-model="statementInputDialogVisible" :title="`${inputDialogTitle} (${logicDomain.toLowerCase()})`"
      :close-on-click-modal="false" :close-on-press-escape="false" :show-close="false">
      <div class="dialogContent">
        <ElInput v-model="newStatement" placeholder="Nový výrok..." clearable />
        <ElAlert v-if="errorMessage" :title="errorMessage" type="error" :closable="false" />
      </div>
      <template #footer>
        <span class="dialog-footer">
          <div class="dialogFooterContainer">
            <ElButtonGroup>
              <ElButton class="logicSymbol" type="info" v-for="sym in getAvailableSymbols()"
                @click="pasteLogicSymbol(sym)">
                {{ sym }}
              </ElButton>
            </ElButtonGroup>
            <ElCheckbox v-model="conclusion" label="Záver" />
            <div>
              <ElButton
                @click="() => { statementInputDialogVisible = false; newStatement = ''; errorMessage = ''; conclusion = false }">
                Zrušiť</ElButton>
              <ElButton type="primary" @click="addStatement">
                Potvrdiť
              </ElButton>
            </div>
          </div>
        </span>
      </template>
    </ElDialog>

    <ElDialog v-model="exampleDialogVisible" :title="'Výber ukážkového príkladu'" :close-on-click-modal="false"
      :close-on-press-escape="false" :show-close="false">
      <div class="dialogContent">
        <ElSelect v-model="selectedExample" placeholder="Výber ukážkového príkladu">
          <ElOption v-for="example in exampleOptions" :value="example.value" :label="example.label" />
        </ElSelect>
      </div>
      <template #footer>
        <div>
          <ElButton @click="() => { exampleDialogVisible = false; selectedExample = '';}">
            Zrušiť</ElButton>
          <ElButton type="primary" @click="useExample">
            Potvrdiť
          </ElButton>
        </div>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import TextInfo from '@/components/TextInfo.vue';
import Statement from '@/components/Statement.vue';
import { DomainType, logicDomain } from '@/script/domain';
import { ElButton, ElDialog, ElInput, ElMessage, ElAlert, ElCheckbox, ElSelect, ElOption } from 'element-plus';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { LogicSymbols, getAvailableSymbols, validateNewStatement, statementList, conclusionIndex, getNLTKSymbol, type ValidationResponse } from '@/script/statement';
import examples from '@/assets/examples.json'
import { SERVER_ERROR_MSG, appHeading } from '@/script/helper';

const ROUTER = useRouter();

const statementInputDialogVisible = ref(false);
const exampleDialogVisible = ref(false);
const inputDialogTitle = ref('Nový výrok');
const newStatement = ref('');
const errorMessage = ref('');
const conclusion = ref(false);
const editStatementOrder = ref(-1);
const selectedExample = ref('');
const exampleOptions: any = [];

function pasteLogicSymbol(symbol: LogicSymbols) {
  const _symbol = getNLTKSymbol(symbol);
  newStatement.value = `${newStatement.value} ${_symbol} `;
}

async function addStatement() {
  const validationResponse: ValidationResponse = { valid: false, errorMessage: '' };

  await validateNewStatement(newStatement.value, validationResponse);

  if (!validationResponse.valid) {
    errorMessage.value = validationResponse.errorMessage;
    return;
  }

  let order: number;
  let elMessagetext: string;
  if (editStatementOrder.value > 0) {
    elMessagetext = 'Výrok bol upravený.';
    order = editStatementOrder.value;

    const _statementIndex = statementList.value.findIndex((_statement) =>
      _statement.order === order
    );

    statementList.value[_statementIndex].statement = newStatement.value;

  } else {
    elMessagetext = 'Výrok bol pridaný.';
    order = statementList.value.length + 1;
    statementList.value.push({ order: order, statement: newStatement.value });
  }

  if (conclusion.value)
    conclusionIndex.value = order;

  errorMessage.value = '';
  newStatement.value = '';
  conclusion.value = false;

  statementInputDialogVisible.value = false;
  ElMessage({
    message: elMessagetext,
    type: 'success',
  });
};

function deleteStatement(order: number) {
  statementList.value = statementList.value.filter((_statement) => {
    return _statement.order !== order;
  });

  statementList.value.forEach(_statement => {
    if (_statement.order > order)
      _statement.order--;
  });

  if (conclusionIndex.value === order)
    conclusionIndex.value = -1;

  ElMessage({
    message: 'Výrok bol vymazaný.',
    type: 'success',
  });
};

function editStatement(order: number) {
  editStatementOrder.value = order;
  statementInputDialogVisible.value = true;
  inputDialogTitle.value = 'Upraviť výrok';

  const _statement = statementList.value.find((_statement) =>
    _statement.order === order
  )?.statement;

  if (!_statement)
    return;

  newStatement.value = _statement;
  if (conclusionIndex.value === order)
    conclusion.value = true;
};

function nextStep() {
if (statementList.value.length < 2) {
    ElMessage({
      message: 'Málo výrokov',
      type: 'error',
    });
    return;
  }

  if (conclusionIndex.value < 0) {
    ElMessage({
      message: 'Záver nie je označený',
      type: 'error',
    });
    return;
  }
  ROUTER.push({ name: 'cnf' });
}

function loadExamples() {
  let _examples;
  if (logicDomain.value === DomainType.PROPOSITIONAL_LOGIC) {
    _examples = examples.propositional.examples;
  } else {
    _examples = examples.predicate.examples;
  }


  _examples.sort((a, b) => a.order - b.order);
  _examples.forEach(example => {
    exampleOptions.push({ value: `${example.order}`, label: example.label })
  });
}

function useExample() {
  statementList.value.length = 0;
  conclusionIndex.value = -1;

  let _examples;
  if (logicDomain.value === DomainType.PROPOSITIONAL_LOGIC) {
    _examples = examples.propositional.examples;
  } else {
    _examples = examples.predicate.examples;
  }

  const e = _examples.find(e => e.order === (+selectedExample.value));
  if (!e) {
    ElMessage({
      message: SERVER_ERROR_MSG,
      type: 'error',
    })
    selectedExample.value = '';
    exampleDialogVisible.value = false;
    return;
  };


  e.statements.forEach((s) => {
    const _order = s.order;
    const _statement = s.statement;
    statementList.value.push({ order: _order, statement: _statement });
  });
  conclusionIndex.value = e.goalIndex;

  exampleDialogVisible.value = false;
  selectedExample.value = '';
}


onMounted(() => {
  loadExamples();
  appHeading.value = 'Zadanie výrokov';
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
  height: 100%;
}

#asideContainer {
  width: fit-content;
  display: flex;
  align-items: center;
}

#mainContainer {
  flex-direction: row-reverse;
  height: 100%;
  max-height: 100%;
  width: 100%;
}

#mainContent {
  width: 100%;
  height: 100%;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

#statements {
  width: 100%;
  height: 100%;
  overflow: scroll;
}

.dialogFooterContainer {
  display: flex;
  justify-content: space-between;
}

.statementList {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.logicSymbol {
  font-size: larger;
}

.dialogContent {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
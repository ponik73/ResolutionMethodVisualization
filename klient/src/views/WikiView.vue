<template>
  <div class="wiki">
    <div class="wikiContent">
      <div class="wikiNav">
        <ul>
          <li @click="redirectWikiSection(ROUTER, 'about')">O stránke</li>
          <li @click="redirectWikiSection(ROUTER, 'resolutionMethod')">Rezolučná metóda</li>
          <li @click="redirectWikiSection(ROUTER, 'resolution')">Rezolúcia</li>
          <li @click="redirectWikiSection(ROUTER, 'searchAlgoritm')">Algoritmus prehľadávania</li>
          <li @click="redirectWikiSection(ROUTER, 'clausularForm')">Klauzulárna forma</li>
        </ul>
      </div>
      <div class="wikiSection" id="about">
        <h3>O stránke</h3>
        <div class="wikiSectionContent">
          <p>Webové stránky s popisom rezolučnej metódy a webovou výukovou aplikáciou, umožňujúcou vizualizáciu
            vykonávanej rezolučnej metódy.</p>
          <p>Stránka v hornej lište zobrazuje odkazy na domovskú stránku a stránku wiki a taktiež stav, v ktorom sa
            výuková aplikácia práve nachádza.</p>
          <p>Pri odborných pojmoch sa nachádza tlačidlo informácie, ktoré zobrazí danú problematiku v stránke wiki.</p>
          <p>Použitie výkovej aplikácie:</p>
          <ol>
            <li>
              <span>Výber domény a algoritmu</span>
              <div class="wikiSectionContent">
                <!-- <p>Pre použitie výukovej aplikácie je nutné zvoliť logickú doménu, v ktorej budú zadávané výroky.</p> -->
                <p>Pre použitie výukovej aplikácie je nutné zvoliť:</p>
                <ol>
                  <li>logickú doménu, v ktorej budú zadávané výroky,</li>
                  <li>algoritmus, ktorým bude vizualizovaná rezolučná metóda riešená.</li>
                </ol>
              </div>
            </li>
            <li>
              <span>Zadanie výrokov</span>
              <div class="wikiSectionContent">
                <p>Na stránke "Zadanie výrokov" je možné zadať výroky, alebo vybrať niektorú sadu ukážkových výrokov</p>
                <p>Výber sady ukážkových výrokov je možný tlačidlom "Príklady", výberom ukážkového príkladu a potvrdením
                  výberu.</p>
                <p>Zadanie vlastného výroku je možné tlačidlom "Pridať výrok", napísaním výroku a potvrdením. Výrok je
                  potom overený a v prípade valídneho výroku pridaný do zoznamu výrokov.
                  <br>
                  <span>Pri zadávaní výrokov je nutné dodržať nasledovnú notáciu:</span>
                  <div class="wikiSectionContent">
                    <ul>
                      <li>
                        výrokové symboly - veľkým písmenom,
                      </li>
                      <li>
                        predikáty - jednoznakové predikáty veľkým písmenom, viac ako jednoznakové predikáty sú valídne aj malými písmenami,
                      </li>
                      <li>
                        funkčné symboly - jednoznakové funkčné symboly veľkým písmenom, viac ako jednoznakové funkčné symboly sú valídne aj malými písmenami,
                      </li>
                      <li>
                        premenné - jednoznakové premenné malým písmenom, viac ako jednoznakové premenné sú valídne malými písmenami alebo s veľkým písmenom na začiatku,
                      </li>
                      <li>
                        konštanty - jednoznakové konštanty malým písmenom, viac ako jednoznakové konštanty sú valídne malými písmenami alebo s veľkým písmenom na začiatku,
                      </li>
                      <li>
                        zátvorky - valídne sú zátvorky '(' a ')'.
                      </li>
                    </ul>
                  </div>
                </p>
              </div>
            </li>
            <li>
              <span>Prevod výrokov do klauzulárnej formy</span>
              <div class="wikiSectionContent">
                <p>Zadané výroky sú upravené do formy vyžadovanej pre dokazovanie pomocou rezolučnej metódy.</p>
                <p>Jednotlivé kroky úpravy sú vizualizované.</p>
              </div>
            </li>
            <li>
              <span>Rezolúcia</span>
              <div class="wikiSectionContent">
                <p>Výroky v klauzulárnej forme vstupujú do procesu rezolúcie.</p>
                <p>Postup procesu rezolúcie je vizualizovaný. Je zobrazený dôkaz pravdivosti dokazovaného záveru a
                  vytvorené rezolventy.</p>
                <p>Pri každej rezolvente sú zobrazené čísla klauzúl, na ktoré bolo potrebné uplatniť rezolučné
                  odvodzovacie pravidlo, aby rezolventa vznikla. Po nabehnutí kurzorom nad čísla rodičovských klauzúl, sú
                  tieto klauzuly zvýraznené a taktiež zobrazené v kontextovom okne. Po kliknutí na číslo rodičovskej
                  klauzuly je klauzula zobrazená.</p>
                <p>Aplikácia ponúka možnosť zobrazenia najkratšieho riešenia tlačidlom "Skrátený dôkaz".</p>
                <p>Tlačidlom "Graf stavového priestoru" je zobrazený postup procesu rezolúcie vo forme grafu stavového
                  priestoru. Ak bol nájdený spor medzi množinou predpokladov a negáciou záveru, je prázdna klauzula
                  označená zelenou farbou.</p>
                <p>Zadanie ďalšieho príkladu je možné tlačidlom "Nový výpočet".</p>
              </div>
            </li>
          </ol>
          <p>Upozornenie: tieto webové stránky sú určené pre zobrazenie s minimálnou šírkou 800px a výškou 500px.</p>
        </div>
      </div>
      <div id="resolutionMethod" class="wikiSection">
        <h3>Rezolučná metóda</h3>
        <div class="wikiSectionContent">
          <p>Rezolučná metóda je významný koncept vo sfére automatického dokazovania. Princíp, na ktorom je rezolučná
            metóda založená, je zistenie pravdivosti dokazovaného výroku hľadaním sporu v konečnej množine klauzúl.</p>
          <p>Rezolučná metóda je úplná dokazovacia metóda, pretože ak je množina logických formulí v klauzárnej forme
            sporná, rezolučná metóda vždy nájde spor v tejto množine.</p>
          <p>V prípade nájdenia sporu medzi záverom a množinou predpokladov, je teda dokazovaný výrok nepravdivý.</p>
        </div>
      </div>
      <div id="resolution" class="wikiSection">
        <h3>Rezolúcia</h3>
        <div class="wikiSectionContent">
          <p>
            Spor je hľadaný procesom, nazývaný rezolúcia, v ktorom sú generované <strong>rezolventy</strong> opakovaným
            uplatňovaním
            <strong>rezolučného odvodzovacieho pravidla</strong> na existujúcu množinu klauzúl, pokiaľ
            nie
            je nájdený spor <strong>negácie</strong>
            dokazovaného výroku s množinou predpokladov, alebo už nie je možné generovať nové klauzuly. Za nájdenie sporu
            je považované odvodenie <strong>prázdnej klauzuly</strong>.
          </p>
          <ul>
            <li>
              <strong>Klauzula</strong> - disjunkcia literálov, kde každý literál je atomická formula alebo
              negácia atomickej formuly.
            </li>
            <li>
              <strong>Rezolventa</strong> - produkt aplikácie rezolučného odvodzovacieho pravidla. Ako špeciálny prípad
              klauzuly je logicky ekvivalentná klauzulám, ktorých zlúčením vznikla.
            </li>
            <li>
              <strong>Rezolučné odvodzovacie pravidlo</strong> - definuje formovanie rezolventy. Ak dve klauzuly obsahujú
              komplementárne (doplnkové) literály, je možné tieto literály zanedbať a zvyšné literály zlúčiť do novej
              klauzuly.
            </li>
            <li>
              <strong>Prázdna klauzula</strong> - špeciálny prípad rezolventy. Neobsahuje žiadny literál a indikuje
              nesplniteľnosť množiny klauzulí.
            </li>
          </ul>
        </div>
      </div>
      <div id="searchAlgoritm" class="wikiSection">
        <h3>Algoritmus prehľadávania</h3>
        <div class="wikiSectionContent">
          <p>Riešenie logického problému, teda prehľadávanie stavového priestoru, musí byť riadené systematickou
            stratégiou.</p>
          <p>Stratégia určuje spôsob generovania stavového stromu.</p>
          <p>Výber vhodnej stratégie ovplyvňuje efektivitu prehľadávania stavového priestoru.</p>
          <p>Táto aplikácia ponúka na výber z týchto algoritmov:</p>
          <ol>
            <li>
              <span> Prehľadávanie do hĺbky (DFS)</span>
              <div class="wikiSectionContent">
                <p>Počiatočným uzlom stratégie prehľadávania do hĺbky, je ľubovoľný neprehľadaný uzol.</p>
                <p>
                  Ak je počiatočný stav zároveň riešením úlohy, algoritmus končí. Ak počiatočný stav nie je riešením,
                  prehľadávanie pokračuje uzlom, ktorý ešte nebol prehľadaný a je v hĺbke nižšej ako práve prehľadaný
                  uzol.
                </p>
                <p>V prípade, že je prehľadávaný stav koncovým stavom (riešením problému) je algoritmus ukončený,
                  inak pokračuje spôsobom popísaným prechodom z počiatočného stavu. Ak nie je možný prechod na
                  neprehľadaný uzol v nižšej hĺbke ako sa algoritmus DFS práve nachádza, pokračuje algoritmus DFS
                  najbližším neprehľadaným potomkom už prehľadaného uzla z menšej hĺbky ako práve prehľadal.</p>
                <p>Algoritmus DFS končí prehľadaním celého stavového priestoru.</p>
              </div>
            </li>
            <li>
              <span> Prehľadávanie do šírky (BFS)</span>
              <div class="wikiSectionContent">
                <p>Algoritmus prehľadávania stavového priestoru do šírky, spočíva v prehľadaní uzlov grafu v rovnakej
                  hĺbke. Na začiatku aplikácie stratégie sú prehľadávané uzly v počiatočnej hĺbke. Hĺbka je počet hrán
                  medzi daným a počiatočným uzlom.</p>
                <p>Ak koreň nie je riešením, sú prehľadávané uzly v hĺbke nižšej o jeden, tak, že ak ani jeden z uzlov nie
                  je riešením algoritmus pokračuje o ďalšiu úroveň nižšie, pokým nenájde riešenie alebo už nie je dostupný
                  žiadny prechod, čiže neexistuje žiadny neprehľadaný stav.</p>
              </div>
            </li>
            <li>
              <span> Algoritmus knižnice NLTK</span>
              <div class="wikiSectionContent">
                <p>Algoritmus knižnice NLTK iteratívne prechádza zoznamom klauzúl a pokúša sa aplikovať rezolučné
                  odvodzovacie pravidlo na klauzulu vybranú v danej iterácii spolu s každou klauzulou, ktorá ju v zozname
                  nasleduje.</p>
                <p> Funkcia si udržiava zoznam “vyskúšaných“
                  kombinácií klauzúl, ktorý reprezentuje dvojicu klauzúl, na ktoré už funkcia uplatnila rezo-
                  lučné odvodzovacie pravidlo. Ak uplatnením rezolučného odvodzovacieho pravidla vznikne
                  rezolventa, je táto novovzniknutá klauzula pridaná na koniec zoznamu klauzúl.</p>
                <p> Ak je utvorená rezolventa, ktorá je zároveň prázdnou klauzulou algoritmus končí.</p>
              </div>
            </li>
          </ol>
        </div>
      </div>
      <div id="clausularForm" class="wikiSection">
        <h3>Klauzulárna forma</h3>
        <div class="wikiSectionContent">
          <p>
            Proces rezolúcie hľadá spor medzi <strong>negáciou</strong> záveru a množinou klauzúl (predpokladov v
            klauzulárnej forme).
          </p>
          <p><strong>Klauzárna forma</strong> logickej formuly je <strong>konjunkcia klauzúl</strong>, ktoré je možné
            sformovať z danej formuly.</p>
          <ul>
            <li>
              <strong>Konjunkcia klauzúl</strong>: klauzuly spojené operátorom (logickou spojkou) <strong>∧</strong>
            </li>
          </ul>
        </div>
        <div id="clausularFormConversion" class="wikiSection">
          <h3>Prevod výrokov do klauzulárnej formy</h3>
          <div class="wikiSectionContent">
            Postup prevodu výroku do klauzulárnej formy:
            <ol>
              <li>
                <span id="cnfRemoveImplications">Odstránenie implikácií</span>
                <div class="wikiSectionContent">
                  <p>Prvou operáciou je zjednodušenie formuly, aby obsahovala iba spojky {{ LogicSymbols.FORALL }}, {{
                    LogicSymbols.EXISTS }}, {{ LogicSymbols.AND }}, {{ LogicSymbols.OR }}, {{ LogicSymbols.NOT }}</p>
                  <table class="wikiTable">
                    <thead>
                      <tr>
                        <th>Formula</th>
                        <th>Zjednodušenie</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>A {{ LogicSymbols.IFF }} B</td>
                        <td>({{ LogicSymbols.NOT }}A {{ LogicSymbols.OR }} B) {{ LogicSymbols.AND }} ({{ LogicSymbols.NOT
                        }}B {{ LogicSymbols.OR }} A)</td>
                      </tr>
                      <tr>
                        <td>A {{ LogicSymbols.IF }} B</td>
                        <td>{{ LogicSymbols.NOT }}A {{ LogicSymbols.OR }} B</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </li>
              <li>
                <span id="cnfRemoveNegations">Odstránenie negácií</span>
                <div class="wikiSectionContent">
                  <table class="wikiTable">
                    <thead>
                      <tr>
                        <th>Formula</th>
                        <th>Zjednodušenie</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{{ `${LogicSymbols.NOT}${LogicSymbols.FORALL}` }}x A</td>
                        <td>{{ LogicSymbols.EXISTS }}x {{ LogicSymbols.NOT }}A</td>
                      </tr>
                      <tr>
                        <td>{{ `${LogicSymbols.NOT}${LogicSymbols.EXISTS}` }}x A</td>
                        <td>{{ LogicSymbols.FORALL }}x {{ LogicSymbols.NOT }}A</td>
                      </tr>
                      <tr>
                        <td>{{ LogicSymbols.NOT }}(A {{ LogicSymbols.AND }} B)</td>
                        <td>({{ LogicSymbols.NOT }}A {{ LogicSymbols.OR }} {{ LogicSymbols.NOT }}B)</td>
                      </tr>
                      <tr>
                        <td>{{ LogicSymbols.NOT }}(A {{ LogicSymbols.OR }} B)</td>
                        <td>({{ LogicSymbols.NOT }}A {{ LogicSymbols.AND }} {{ LogicSymbols.NOT }}B)</td>
                      </tr>
                      <tr>
                        <td>{{ `${LogicSymbols.NOT}${LogicSymbols.NOT}` }}A</td>
                        <td>A</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </li>
              <li>
                <span id="cnfSkolemize">Skolemizácia a odstránenie univerzálnych kvantifikátor</span>
                <div class="wikiSectionContent">
                  <p>Skolemizácia odstráni existenčné kvantifikátory {{ LogicSymbols.EXISTS }}.</p>
                  <p>V tomto kroku sa existenčne kvantifikované premenné
                    nahradia takým funkčným symbolom, ktorý ešte nebol vo formule
                    použitý a jeho argumentmi sú všetky premenné viazané na univerzálne kvantifikátory {{
                      LogicSymbols.FORALL }} v <strong>prenexnom bloku</strong>.
                  </p>
                  <p>Všetky premenné, ktoré zostanú po skolemizácii,
                    sú implicitne univerzálne kvantifikované.</p>
                  <p>Po skolemizácii je formula v
                    prenexnej normálnej forme zbavená existenčných kvantifikátorov</p>
                  <p>Univerzálne kvantifikátory sú odstránené pomocou axiómu {{ LogicSymbols.FORALL }}x A {{
                    LogicSymbols.IF }} A[x/t]. Unverzálny kvantifikátor {{ LogicSymbols.FORALL }} môže byť odstránený, ak
                    je premenná x nahradená premennou t (substitúcia).</p>
                  <ul>
                    <li>
                      <strong>Prenexná normálna forma</strong> - spôsob organizovania kvantifikátorov formuly do
                      prenexného bloku, t.j. skupina kvantifikátorov na začiatku formuly. Ak sa v prenexnom bloku
                      vyskytujú existenčné kvantifikátory, ich miesto je vždy na konci bloku.
                    </li>
                  </ul>
                </div>
              </li>
              <li>
                <span id="cnfCnf">Konjunktívna normálna forma</span>
                <div class="wikiSectionContent">
                  <p>
                    Rozdelenie disjunkcií tak, aby formule boli konjunkciami disjunkcií. Po rozdelení
                    disjunkcií sú formuly v konjunktívnej normálnej forme.
                  </p>
                  <table class="wikiTable">
                    <thead>
                      <tr>
                        <th>Formula</th>
                        <th>Konjunktívna normálna forma</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>A {{ LogicSymbols.OR }} (B {{ LogicSymbols.AND }} C)</td>
                        <td>(A {{ LogicSymbols.OR }} B) {{ LogicSymbols.AND }} (A {{ LogicSymbols.OR }} C)</td>
                      </tr>
                      <tr>
                        <td>(B {{ LogicSymbols.AND }} C) {{ LogicSymbols.OR }} A</td>
                        <td>(B {{ LogicSymbols.OR }} A) {{ LogicSymbols.AND }} (C {{ LogicSymbols.OR }} A)</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </li>
              <li>
                <span id="cnfFinish">Klauzulárna forma</span>
                <div class="wikiSectionContent">
                  <p>Poslednou operáciou je prevod do normálneho tvaru klauzuly. To sa vykoná odstránením konjunkcií, čím
                    sa vytvorí množina klauzúl.</p>
                  <p>Formula: P<sub>1</sub> {{ LogicSymbols.AND }} ... {{ LogicSymbols.AND }} P<sub>n</sub></p>
                  <p>Klauzulárna forma: {P<sub>1</sub>, ..., P<sub>n</sub>}</p>
                </div>
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
    <ElBacktop :right="80" :bottom="100" />
  </div>
</template>

<script setup lang="ts">
import { appHeading, redirectWikiSection } from '@/script/helper';
import { LogicSymbols } from '@/script/statement';
import type { ElBacktop, ElLink } from 'element-plus';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const ROUTER = useRouter();

onMounted(() => {
  appHeading.value = 'Rezolučná metóda';
})
</script>

<style scoped>
.wiki {
  height: 100%;
  max-height: 90%;
  position: relative;
  width: 100%;
  max-width: var(--max-width);
  scroll-behavior: smooth;
}

.wiki ul,
ol {
  margin-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.wikiNav {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  width: calc(100% - 10px);
  padding: 5px;
  margin-bottom: 5px;
  background-color: #A3A6AD;
  display: flex;
  gap: 20px;
}

.wikiNav ul {
  list-style: none;
  display: flex;
  flex-direction: row;
  gap: 20px;
  color: var(--el-bg-color-page);
  margin: 0;
}

.wikiNav ul li:hover {
  text-decoration: underline;
  cursor: pointer;
}

.wikiNav .el-link:hover::after {
  border-color: var(--el-bg-color-page);
}

.wikiContent {
  display: flex;
  flex-direction: column;
  gap: 50px;
  padding-bottom: 80px;
  width: 100%;
  max-width: var(--max-width);
  scroll-behavior: smooth;
}

.wikiSection h3 {
  color: #CFD3DC;
}

.wikiSection {
  color: #A3A6AD;
  padding-right: 30px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.wikiSectionContent {
  display: flex;
  flex-direction: column;
  gap: 10px;
  line-height: 1.5;
}

.wikiSectionContent ul {
  list-style: disc;
}

.wikiTable {
  border: 1px solid #CFD3DC;
  width: max-content;
}

.wikiTable td,
.wikiTable th {
  border: 1px solid #CFD3DC;
  padding: 5px;
}
</style>
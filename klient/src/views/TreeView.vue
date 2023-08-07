<template>
    <div id="viewContainer">
        <div id="mynetwork"></div>
    </div>
</template>

<script setup lang="ts">
import type { SolutionNode } from "@/script/resolution";
import { solutionFull } from "@/script/resolution";
import { statementList } from "@/script/statement";
import { Network, type Edge, type Node } from "vis-network/standalone";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const ROUTER = useRouter();

const resolvents = ref<SolutionNode[]>([]);

function drawGraph() {

    const container = document.getElementById("mynetwork");
    if (!container)
        return;

    const root = solutionFull.value.find(node => node.order === 1);
    if (!root)
        return;

    const nodes: Node[] = [];

    const edges: Edge[] = [];

    const nodeFontSize = 20;
    const edgeFontSize = 25;

    nodes.push({ id: 0, label: '', font: { size: nodeFontSize } });

    solutionFull.value.forEach(node => {
        if (node.parents.length === 2) {
            nodes.push({ id: node.order, label: `${node.order}`, font: { size: nodeFontSize } })
            if (node.clause === '\u2610')
            {
                nodes.pop()
                nodes.push({ id: node.order, label: `${node.clause}`, font: { size: nodeFontSize, color: '#CFD3DC' }, color: { background: '#3e6b27' }, })
            }
            edges.push({ from: node.parents[0], to: node.order, label: `${node.parents[1]}`, font: { size: edgeFontSize, color: '#CFD3DC', strokeColor: 'black' } })
        } else if (node.parents.length === 1) {
            nodes.push({ id: node.order, label: `${node.order}`, font: { size: nodeFontSize } })
            edges.push({ from: 0, to: node.order, label: '', font: { size: edgeFontSize, color: '#CFD3DC', strokeColor: 'black' } })
        }
    });

    const data = {
        nodes: nodes,
        edges: edges,
    };
    console.log(data);

    let options = {
        layout: {
            hierarchical: {
                direction: "UD",//"LR",
                sortMethod: "directed",
                shakeTowards: 'roots' //'leaves'
            },
        },
        interaction: { dragNodes: false },
        physics: {
            enabled: false,
        },
        edges: {
            arrows: "to",
        },
    };
    let network = new Network(container, data, options);
}

onMounted(async () => {
    if (statementList.value.length < 2) {
        ROUTER.replace({ name: 'home' });
        return;
    }
    const _resolvents = solutionFull.value.filter(node => {
        return node.parents.length === 2
    })
    _resolvents.forEach(node => {
        resolvents.value.push(node)
    });
    drawGraph();

})
</script>

<style scoped>
#viewContainer {
    width: 100%;
    max-width: var(--max-width);
    height: 100%;
    max-height: 90%;
}

#mynetwork {
    width: 100%;
    height: 100%;
    border: 1px solid #CFD3DC;
}
</style>
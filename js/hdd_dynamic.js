import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "HDD.DynamicNodes",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "HDD_RandomPromptMatcher") {
            
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info, slot_info) {
                if (onConnectionsChange) onConnectionsChange.apply(this, arguments);

                if (type !== 1) return;
                if (this.adjusting_slots) return;

                const inputPrefix = "次要输入_";
                
                let secondarySlots = [];
                for (let i = 0; i < this.inputs.length; i++) {
                    if (this.inputs[i].name.startsWith(inputPrefix)) {
                        const parts = this.inputs[i].name.split("_");
                        const num = parseInt(parts[1]);
                        secondarySlots.push({ index: i, num: num, link: this.inputs[i].link });
                    }
                }
                
                secondarySlots.sort((a, b) => a.num - b.num);
                
                if (secondarySlots.length === 0) return;

                const lastSlot = secondarySlots[secondarySlots.length - 1];
                const maxNum = lastSlot.num;

                this.adjusting_slots = true; 

                // 增加逻辑
                if (lastSlot.link !== null) {
                    this.addInput(`${inputPrefix}${maxNum + 1}`, "STRING");
                }
                // 减少逻辑
                else if (secondarySlots.length > 1) {
                    const secondLastSlot = secondarySlots[secondarySlots.length - 2];
                    if (lastSlot.link === null && secondLastSlot.link === null) {
                        this.removeInput(lastSlot.index);
                    }
                }

                this.adjusting_slots = false;
            };
        }
    }
});
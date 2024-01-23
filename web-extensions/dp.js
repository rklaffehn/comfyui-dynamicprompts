import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

import { DP_RandomPromptGenerator, DP_FeelingLuckyGenerator, DP_MagicPromptGenerator } from "./dp_random.js";

// It is currently not possible to disable the built-in dynamic prompts-like syntax in ComfyUI.
// Until that is fixed, this extension is used to disable it.
const id = "DP.PromptWidget";
app.registerExtension({
  name: id,
  addCustomNodeDefs(node_defs) {
    ComfyWidgets["PROMPT"] = function(node, inputName, inputData, app) {
      let stringWidget = ComfyWidgets["STRING"](node, inputName, inputData, app);
      stringWidget.widget.dynamicPrompts = false;

      return stringWidget;
    }
  },

  registerCustomNodes(app) {
    LiteGraph.registerNodeType(
      "DP_RandomPromptGenerator",
      Object.assign(DP_RandomPromptGenerator, {
        title_mode: LiteGraph.NORMAL_TITLE,
        title: "Random Prompt (Server)",
        collapsable: true,
      })
    );
    DP_RandomPromptGenerator.category = "Dynamic Prompts";

    LiteGraph.registerNodeType(
      "DP_FeelingLuckyGenerator",
      Object.assign(DP_FeelingLuckyGenerator, {
        title_mode: LiteGraph.NORMAL_TITLE,
        title: "Feeling Lucky (Server)",
        collapsable: true,
      })
    );
    DP_FeelingLuckyGenerator.category = "Dynamic Prompts";

    LiteGraph.registerNodeType(
      "DP_MagicPromptGenerator",
      Object.assign(DP_MagicPromptGenerator, {
        title_mode: LiteGraph.NORMAL_TITLE,
        title: "Magic Prompt (Server)",
        collapsable: true,
      })
    );
    DP_MagicPromptGenerator.category = "Dynamic Prompts";
  },
});

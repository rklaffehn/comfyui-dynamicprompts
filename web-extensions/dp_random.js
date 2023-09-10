import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { ComfyWidgets } from "../../scripts/widgets.js";
import { forwardOutputValues } from "../core/utilities.js";

/** A class template prototype to generate random prompts by querying the dynamicprompts/random end-point.
 */
export class DP_RandomPromptGenerator {
  constructor() {
    this.parameters = {
      current_template: null,
      template: ComfyWidgets.PROMPT(
        this,
        "template",
        ["", { default: "", multiline: true, dynamicPrompts: false }],
        app
      ).widget,
      prompt: ComfyWidgets.PROMPT(this, "prompt", ["", { default: "", multiline: true, dynamicPrompts: false }], app)
        .widget,
    };

    this.addOutput("prompt", "STRING", "");

    this.serialize_widgets = true;
    this.isVirtualNode = true;
  }

  onConfigure() {
    this.#queryRandomPrompt();
  }

  onSerialize() {
    const current_template = this.parameters.template.value;
    if (this.parameters.last_template != current_template) {
      this.#updatePromptAndForward();
    }
  }

  applyToGraph() {
    /* Note the reversed order. Here, we want to forward the existing prompt (if needed) and update to a new one afterward. */
    forwardOutputValues(this, (output) => this.parameters.prompt.value);
    this.#queryRandomPrompt();
  }

  async #queryRandomPrompt() {
    const current_template = this.parameters.template.value;
    const response = await api.fetchApi("/dynamicprompts/random", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ template: current_template }),
    });
    
    this.parameters.last_template = current_template;

    if (response.ok) {
      const prompt = await response.json();
      this.parameters.prompt.value = prompt.prompt;
    } else {
      this.parameters.prompt.value = `ERROR: ${response.statusText}`;
      throw new Error(`failed to generate a prompt from the template:\n${response.statusText}`);
    }
  }

  #updatePromptAndForward() {
    this.#queryRandomPrompt();
    forwardOutputValues(this, (output) => this.parameters.prompt.value);
  }
}

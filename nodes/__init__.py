from .combinatorial import DPCombinatorialGenerator
from .feeling_lucky import DPFeelingLucky
from .jinja import DPJinja
from .magicprompt import DPMagicPrompt
from .output_node import OutputString
from .random import DPRandomGenerator

from .dp_server import dp_server

NODE_CLASS_MAPPINGS = {
    "DPRandomGenerator": DPRandomGenerator,
    "DPCombinatorialGenerator": DPCombinatorialGenerator,
    "DPFeelingLucky": DPFeelingLucky,
    "DPJinja": DPJinja,
    "DPMagicPrompt": DPMagicPrompt,
    "DPOutput": OutputString,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "DPRandomGenerator": "Random Prompts",
    "DPCombinatorialGenerator": "Combinatorial Prompts",
    "DPFeelingLucky": "I'm Feeling Lucky",
    "DPJinja": "Jinja2 Templates",
    "DPMagicPrompt": "Magic Prompt",
    "DPOutput": "OutputString",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

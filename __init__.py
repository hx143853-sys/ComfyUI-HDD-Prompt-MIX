from .hdd_nodes import HDD_RandomPromptMatcher

NODE_CLASS_MAPPINGS = {
    "HDD_RandomPromptMatcher": HDD_RandomPromptMatcher
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HDD_RandomPromptMatcher": "HDD🤣 随机提示词匹配器"
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
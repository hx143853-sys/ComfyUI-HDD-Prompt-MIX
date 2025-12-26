import random

class HDD_RandomPromptMatcher:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "主提示词": ("STRING", {"multiline": True, "default": "", "placeholder": "主提示词（固定不变的内容）"}),
                "连接符": ("STRING", {"default": ",", "multiline": False}),
                # Seed 控件：控制每一次随机选择的结果
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "label": "随机种子"}),
            },
            "optional": {
                # 初始次要输入
                "次要输入_1": ("STRING", {"forceInput": True, "multiline": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("HDD🤣_最终文本",)
    FUNCTION = "process_text"
    CATEGORY = "HDD🤣_Nodes"
    
    def process_text(self, 主提示词, 连接符, seed, unique_id=None, extra_pnginfo=None, **kwargs):
        
        # 1. 初始化随机生成器
        rng = random.Random(seed)
        
        selected_parts = []

        # 2. 按照顺序（次要输入_1, 次要输入_2...）处理每一个输入框
        # 我们必须排序，保证拼接顺序是 1->2->3 而不是乱的
        sorted_keys = sorted(kwargs.keys(), key=lambda x: int(x.split('_')[1]) if '_' in x and x.split('_')[1].isdigit() else 9999)
        
        for key in sorted_keys:
            if key.startswith("次要输入_"):
                text_block = kwargs[key]
                
                # 只有当输入是字符串且不为空时才处理
                if isinstance(text_block, str) and text_block.strip() != "":
                    # 按行分割
                    lines = text_block.split('\n')
                    # 过滤空行
                    valid_lines = [line.strip() for line in lines if line.strip()]
                    
                    if valid_lines:
                        # --- 核心修改：针对【当前】这个输入框，随机抽一行 ---
                        chosen_line = rng.choice(valid_lines)
                        selected_parts.append(chosen_line)

        # 3. 组合最终文本
        # 先把所有次要部分拼起来
        secondary_combined = 连接符.join(selected_parts)
        
        # 再和主提示词拼起来
        if 主提示词.strip() and secondary_combined:
            final_text = f"{主提示词}{连接符}{secondary_combined}"
        elif secondary_combined:
            final_text = secondary_combined
        else:
            final_text = 主提示词

        return (final_text,)
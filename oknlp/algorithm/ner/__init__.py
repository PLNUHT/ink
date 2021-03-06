from typing import List
from .BaseNER import BaseNER
from .bert_ner import BertNER


def get_ner(name: str = "") -> BaseNER:
    """根据条件获取一个NER类的实例，无法根据条件获取时返回BertNER()

    Args:
        name: str，表示NER类使用到的方法，目前支持: "bert"
    """
    name = name.lower()
    if name == "bert":
        return BertNER()
    return BertNER()


def get_all_ner() -> List[BaseNER]:
    """获取所有NER类的实例
    """
    return [BertNER()]

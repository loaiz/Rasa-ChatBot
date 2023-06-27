from typing import List


def list_to_nl(ls: List[str]) -> str:
    if not ls:
        return ""
    text = ls[0]
    if len(ls) > 1:
        for e in ls[1:-1]:
            text += f", {e}"
        text += f", and {ls[-1]}"
    return text

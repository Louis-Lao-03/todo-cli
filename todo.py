
"""A tiny todo list, standard library only."""
import sys
from pathlib import Path

DB = Path("todos.txt")


def load() -> list[str]:
    if not DB.exists():
        return []
    return [line.rstrip("\n") for line in DB.read_text(encoding="utf-8").splitlines()]


def save(items: list[str]) -> None:
    text = "\n".join(items)
    if text:
        text += "\n"
    DB.write_text(text, encoding="utf-8")


def add(text: str) -> None:
    items = load()
    items.append(text)
    save(items)
    print(f"added: {text}")


def show() -> None:
    items = load()
    if not items:
        print("nothing to do")
        return
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")
    print(f"共 {len(items)} 项")


def done(index: int) -> bool:
    items = load()
    if index < 1 or index > len(items):
        print("no such item", file=sys.stderr)
        return False
    del items[index - 1]
    save(items)
    print(f"done: {index}")
    return True


def remove(index: int) -> bool:
    items = load()
    if index < 1 or index > len(items):
        print("no such item", file=sys.stderr)
        return False
    del items[index - 1]
    save(items)
    print(f"removed: {index}")
    return True


def all_items() -> list[str]:
    """Return every todo."""
    return load()



def main(argv: list[str]) -> int:
    if len(argv) < 2:
        show()
        return 0
    command, *rest = argv[1:]
    if command == "add" and rest:
        add(" ".join(rest))
    elif command == "list":
        show()
    elif command == "done" and rest:
        try:
            index = int(rest[0])
        except ValueError:
            index = 0
        if not done(index):
            return 1
    elif command == "remove" and rest:
        try:
            index = int(rest[0])
        except ValueError:
            index = 0
        if not remove(index):
            return 1
    else:
        print(f"unknown command: {command}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

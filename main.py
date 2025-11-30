import importlib

for day in range(1,2):
    module = importlib.import_module(f"day{day}")
    run = getattr(module, "run")
    run(open("input/day{day}"))
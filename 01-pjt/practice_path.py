from pathlib import Path

here = Path.cwd()
print(here)

filename = 'output/reading_habits.json'
print(here / filename)

home = Path.home()
print(home)

# 하위 폴더 찾는 방법
for item in here.iterdir():
    print(item.name)
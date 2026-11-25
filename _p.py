import json
with open(r'd:\New folder\temp_repo\temp_repo.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Add Bird class to Q1
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and any('class Cat(Animal):' in s for s in cell.get('source', [])):
        cell['source'].append("\n")
        cell['source'].append("class Bird(Animal):\n")
        cell['source'].append("    def fly(self):\n")
        cell['source'].append('        print(f"{self.name} is flying!")\n')
        cell['source'].append("\n")
        cell['source'].append('    def __repr__(self):\n')
        cell['source'].append('        return f"Bird({self.name})"\n')
        cell['source'].append("\n")
        cell['source'].append('my_bird = Bird("Tweety")\n')
        cell['source'].append("my_bird.make_sound()\n")
        cell['source'].append("my_bird.fly()\n")
        cell['source'].append("print(repr(my_bird))\n")
        break

with open(r'd:\New folder\temp_repo\temp_repo.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
    f.write('\n')
print("done")

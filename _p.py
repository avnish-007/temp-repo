import json
with open(r'd:\New folder\temp_repo\temp_repo.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Add Teacher subclass to Q2 (Person/Student cell)
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and any('class Student(Person):' in s for s in cell.get('source', [])):
        cell['source'] = [
            line.replace(
                '# Solution\n',
                'class Teacher(Person):\n'
                '    def __init__(self, name: str, age: int, subject: str):\n'
                '        super().__init__(name, age)\n'
                '        self.subject = subject\n'
                '\n'
                '    def __str__(self):\n'
                '        return f"{self.name} teaches {self.subject}"\n'
                '\n'
                '# Solution\n'
            ) for line in cell['source']
        ]
        cell['source'].append("\n")
        cell['source'].append('teacher = Teacher("Dr. Smith", 45, "Physics")\n')
        cell['source'].append("print(teacher)\n")
        break

with open(r'd:\New folder\temp_repo\temp_repo.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
    f.write('\n')
print("done")

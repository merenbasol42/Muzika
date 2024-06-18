import os

from program import Program

running_dir = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    os.pardir
)
program = Program(running_dir=running_dir)
print(f"running dir: {program.RUNNING_DIR}")
program.start()





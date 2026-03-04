from geometric_lib import circle
from geometric_lib import square

config = {}

with open ("/app/config/config.txt") as f:
    for line in f:
        key, val = line.strip().split('=')
        config[key] = val
        
shape = config["shape"]
val = float(config["value"])
if shape == 'circle':
    print(f"Circle area: {circle.area(val)}")
    print(f"Circle perimeter: {circle.perimeter(val)}")
elif shape == 'square':
    print(f"Square area: {square.area(val)}")
    print(f"Square perimeter: {square.perimeter(val)}")
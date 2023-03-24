# iremover [![GitHub license](https://img.shields.io/github/license/pchchv/iremover.svg)](https://github.com/pchchv/iremover/blob/master/LICENSE) [![PyPi](https://img.shields.io/pypi/v/iremover?style=flat-square)](https://pypi.org/project/iremover/)
Image background remover

## Requirements 

```
python: >3.7
```

## Installation

```bash
pip install iremover
```

## Usage as a cli

After installation, iiremover can be used simply by typing `iremover` in the terminal window.

The `iremover` command has 3 subcommands, one for each input type:
- `i` for files 
    * ```iremover i path/to/input.png path/to/output.png```
- `p` for folders
    * ```iremover p path/to/input path/to/output```
- `s` for http server
    * ```curl -s "http://localhost:5000/?url=http://input.png" -o output.png```

A reference about the main team can be obtained by using:

```bash
iremover --help
```

And also about all the subcommands used:

```bash
iremover <COMMAND> --help
```

## Usage as a library

Input and output as bytes

```python
from iremover import remove

input_path = 'input.png'
output_path = 'output.png'

with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)
```

Input and output as a PIL image

```python
from iremover import remove
from PIL import Image

input_path = 'input.png'
output_path = 'output.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)
```

Input and output as a numpy array

```python
from iremover import remove
import cv2

input_path = 'input.png'
output_path = 'output.png'

input = cv2.imread(input_path)
output = remove(input)
cv2.imwrite(output_path, output)
```

How to iterate over files in a performatic way

```python
from pathlib import Path
from iremover import remove, new_session

session = new_session()

for file in Path('path/to/folder').glob('*.png'):
    input_path = str(file)
    output_path = str(file.parent / (file.stem + ".out.png"))

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input, session=session)
            o.write(output)
```
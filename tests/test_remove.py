from io import BytesIO
from pathlib import Path

from imagehash import average_hash
from PIL import Image

from iremover import remove

here = Path(__file__).parent.resolve()


def remover(image, expected):
    actual = remove(image)

    actual_hash = average_hash(Image.open(BytesIO(actual)))
    expected_hash = average_hash(Image.open(BytesIO(expected)))

    assert actual_hash == expected_hash

def test_remove():
    for i in range (1, 6):
        image = Path(here / "." / "img" / str(i) + '.jpg' ).read_bytes()
        expected = Path(here / "." / "img" / str(i) + '.out.png').read_bytes()

        remover(image, expected)

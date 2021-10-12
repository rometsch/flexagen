#!/usr/bin/env python3
""" Create a hexa-tetraflexagon from six images. """
import argparse

from PIL import Image


def main():

    parser = argparse.ArgumentParser(description="Create a hexa-tetraflexagon from six same sized images.")
    parser.add_argument("imgdir", type=str,
                        help="Dir containing images named 1-6.png")
    options = parser.parse_args()

    imgdir = options.imgdir

    img = Image.open(f"{imgdir}/1.png")
    L = img.size[0]

    front = Image.new("RGBA", (2*L, 2*L), color=(255, 255, 255))
    back = Image.new("RGBA", (2*L, 2*L), color=(255, 255, 255))

    for n in range(6):
        img = Image.open(f"{imgdir}/{n+1}.png")
        quarters = quarter_img(img, L)

        for k in range(4):
            m = facemap[(n, k)]
            side = m[0]
            pos = positions[m[1]]
            angle = m[2]

            coords = (pos[0]*L//2, pos[1]*L//2)

            if side == "F":
                target = front
            else:
                target = back

            p = quarters[k]
            if angle != 0:
                if angle == 90:
                    # PIL rotates counter clockwise, so flip
                    trafo = Image.ROTATE_270
                elif angle == 180:
                    trafo = Image.ROTATE_180
                elif angle == 270:
                    trafo = Image.ROTATE_90
                p = p.transpose(trafo)

            target.paste(p, coords)

    front.save("front.png")
    back.save("back.png")


def quarter_img(img, L):
    """ Split the image into quarters.

    The quarters are counted clockwise starting in the top left.
        ---- ----
       | c1 | c2 |
        ---- ----
       | c3 | c4 |
        ---- ----

    Parameters
    ----------
    img: PIL.Image
        Image to be split.

    Returns
    -------
    list of PIL.Image
        Images containing the quarters.
    """
    c1 = img.crop((0, 0, L/2, L/2))
    c2 = img.crop((L/2, 0, L, L/2))
    c3 = img.crop((L/2, L/2, L, L))
    c4 = img.crop((0, L/2, L/2, L))

    return [c1, c2, c3, c4]


# mapping from flat sides as they appear in the finished flexagon to the initial schematic
# nomenclature is like follows
#
#    ---- ----
#   | N1 | N2 |
#    ---- ----
#   | N3 | N4 |
#    ---- ----
#
# where X stands for the side (back (B) or front (F))
#

# entries (side, position, angle)
facemap = {
    (2, 0): ("F", 0, 0),
    (2, 1): ("F", 1, 0),
    (3, 2): ("F", 2, 90),
    (5, 0): ("F", 3, 90),
    (5, 1): ("F", 4, 90),
    (3, 3): ("F", 5, 270),
    (2, 2): ("F", 6, 0),
    (2, 3): ("F", 7, 0),
    (3, 0): ("F", 8, 90),
    (5, 2): ("F", 9, 90),
    (5, 3): ("F", 10, 90),
    (3, 1): ("F", 11, 270),
    (4, 1): ("B", 0, 180),
    (4, 0): ("B", 1, 180),
    (0, 1): ("B", 2, 90),
    (1, 1): ("B", 3, 270),
    (1, 0): ("B", 4, 270),
    (0, 0): ("B", 5, 270),
    (4, 3): ("B", 6, 180),
    (4, 2): ("B", 7, 180),
    (0, 3): ("B", 8, 90),
    (1, 3): ("B", 9, 270),
    (1, 2): ("B", 10, 270),
    (0, 2): ("B", 11, 270)
}

positions = {
    0: (0, 0),
    1: (1, 0),
    2: (2, 0),
    3: (3, 0),
    4: (3, 1),
    5: (3, 2),
    6: (3, 3),
    7: (2, 3),
    8: (1, 3),
    9: (0, 3),
    10: (0, 2),
    11: (0, 1)
}


if __name__ == "__main__":
    main()

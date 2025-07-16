class BoundingBox():
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def as_tuple(self):
        return (self.left, self.bottom, self.right, self.top)


GRUITHUISEN_DOMES_GCS = BoundingBox(
    left=-46,
    bottom=31,
    right=-34,
    top=43
)

GRUITHUISEN_DOMES_EDCM = BoundingBox(
    left=-1394000,
    bottom=939000,
    right=-1031000,
    top=1301000
)

search_gcs = {
    'Gruithuisen Domes': GRUITHUISEN_DOMES_GCS.as_tuple(),
}

search_edcm = {
    'Gruithuisen Domes': GRUITHUISEN_DOMES_EDCM.as_tuple(),
}

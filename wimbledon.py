import numpy


def ratings(records):
    transpose = records.transpose()
    symmetric = records + transpose
    A = numpy.diag(symmetric.sum(0)) - symmetric
    b = (transpose - records).sum(0) * 2
    return numpy.linalg.lstsq(A, b, rcond=None)[0]


def chances(ratings):
    return 1 / (1 + numpy.exp(ratings[None, :] - ratings[:, None]))

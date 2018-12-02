import DirectNotifyGlobal, Mersenne

def randHash(num):
    rng = RandomNumGen(num)
    return rng.randint(0, 1 << 16)


class RandomNumGen:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('RandomNumGen')

    def __init__(self, seed):
        if isinstance(seed, RandomNumGen):
            rng = seed
            seed = rng.randint(0, 1L << 16)
        self.notify.debug('seed: ' + str(seed))
        seed = int(seed)
        rng = Mersenne.Mersenne(seed)
        self.__rng = rng

    def __rand(self, N):
        return int(self.__rng.getUint31() * long(N) >> 31)

    def choice(self, seq):
        return seq[self.__rand(len(seq))]

    def shuffle(self, x):
        for i in xrange(len(x) - 1, 0, -1):
            j = int(self.__rand(i + 1))
            x[i], x[j] = (x[j], x[i])

    def randrange(self, start, stop=None, step=1):
        istart = int(start)
        if istart != start:
            raise ValueError, 'non-integer arg 1 for randrange()'
        if stop is None:
            if istart > 0:
                return self.__rand(istart)
            raise ValueError, 'empty range for randrange()'
        istop = int(stop)
        if istop != stop:
            raise ValueError, 'non-integer stop for randrange()'
        if step == 1:
            if istart < istop:
                return istart + self.__rand(istop - istart)
            raise ValueError, 'empty range for randrange()'
        istep = int(step)
        if istep != step:
            raise ValueError, 'non-integer step for randrange()'
        if istep > 0:
            n = (istop - istart + istep - 1) / istep
        else:
            if istep < 0:
                n = (istop - istart + istep + 1) / istep
            else:
                raise ValueError, 'zero step for randrange()'
        if n <= 0:
            raise ValueError, 'empty range for randrange()'
        return istart + istep * int(self.__rand(n))
        return

    def randint(self, a, b):
        range = b - a + 1
        r = self.__rand(range)
        return a + r

    def random(self):
        return float(self.__rng.getUint31()) / float(1L << 31)
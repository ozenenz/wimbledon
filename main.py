# www.tennis-data.co.uk
# en.wikipedia.org/wiki/ATP_Rankings#Ranking_method
# en.wikipedia.org/wiki/WTA_Rankings#Ranking_method


def cached_property(f):
    from functools import lru_cache
    return property(lru_cache()(f))


class Records:
    def __init__(self, records):
        self.records = records

    @cached_property
    def ratings(self):
        from wimbledon import ratings
        return ratings(self.records)

    @cached_property
    def chances(self):
        from wimbledon import chances
        return chances(self.ratings)


class Data:
    def __init__(self, files):
        from glob import glob
        self.files = sorted(glob('data/' + files + '.csv'))

    @cached_property
    def frames(self):
        from pandas import read_csv
        return [read_csv(f) for f in self.files]

    @cached_property
    def players(self):
        ret = set()
        for f in self.frames:
            ret.update(f['Winner'])
            ret.update(f['Loser'])
        return {n: i for i, n in enumerate(sorted(ret))}

    @cached_property
    def records(self):
        from numpy import zeros
        records = []
        for frame in self.frames:
            record = zeros((len(self.players), len(self.players)))
            for _, r in frame.iterrows():
                record[self.players[r['Winner']]
                       ][self.players[r['Loser']]] += 1
            records.append(record)
        return records

def getProfit(players, record, frame):
    import wimbledon
    chances = wimbledon.chances(wimbledon.ratings(record))
    profit = []
    for _, r in frame.iterrows():
        w, l = players[r['Winner']], players[r['Loser']]
        ew, el = chances[w][l]*r['MaxW'], chances[l][w]*r['MaxL']
        profit.append(r['MaxW'] if ew > el else 0)
    return sum(profit)/len(profit)-1

data = Data('M*')
print(getProfit(data.players, sum(data.records[:-1]), data.frames[-1]))

# print(pandas.concat(frames)[['BbAvH', 'BbAvD', 'BbAvA']].describe())
# print(frame.Tier.value_counts())
# print(frame.Series.value_counts())

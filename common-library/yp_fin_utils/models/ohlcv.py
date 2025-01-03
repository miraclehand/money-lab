from pymodm import fields, EmbeddedMongoModel


class Ohlcv(EmbeddedMongoModel):
    date  = fields.DateTimeField(required=True)
    close = fields.FloatField(required=True)
    open  = fields.FloatField()
    high  = fields.FloatField()
    low   = fields.FloatField()
    volume= fields.FloatField()
    diff  = fields.FloatField()
    change= fields.FloatField()
    log   = fields.FloatField()

    def __init__(self, date=None, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return

        self.date  = date
        self.close = newone['close']
        self.open  = newone['open']
        self.high  = newone['high']
        self.low   = newone['low']
        self.volume= newone['volume']
        self.diff  = newone['diff']
        self.change= newone['change']
        self.log   = newone['log']

    @property
    def to_dict(self):
        return {
            'date'  : self.date.date(),
            'close' : self.close,
            'open'  : self.open,
            'high'  : self.high,
            'low'   : self.low,
            'volume': self.volume,
            'diff'  : self.diff,
            'change': self.change,
            'log'   : self.log
        }

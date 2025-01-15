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

    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return

        self.date  = newone.get('date')
        self.close = newone.get('close')
        self.open  = newone.get('open')
        self.high  = newone.get('high')
        self.low   = newone.get('low')
        self.volume= newone.get('volume')
        self.diff  = newone.get('diff')
        self.change= newone.get('change')
        self.log   = newone.get('log')

    @property
    def to_dict(self):
        return {
            'date'  : self.date.date().isoformat(),
            'close' : self.close,
            'open'  : self.open,
            'high'  : self.high,
            'low'   : self.low,
            'volume': self.volume,
            'diff'  : self.diff,
            'change': self.change,
            'log'   : self.log
        }

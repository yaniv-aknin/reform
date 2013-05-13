import csv
import json

class BadLine(Exception): pass


class BaseHandler(object):
    SUFFIX = None
    @classmethod
    def implementations(cls):
        def mangle_name(s):
            s = s[:-len(cls.SUFFIX)] if cls.SUFFIX and s.endswith(cls.SUFFIX) else s
            return s.lower()
        return {mangle_name(cls.__name__): cls for cls in cls.__subclasses__()}


class BaseInputHandler(BaseHandler):
    SUFFIX = 'InputHandler'
    def __init__(self, stream):
        self.stream = stream
    def __iter__(self):
        for index, read_data in enumerate(self.stream):
            yield self.handle(index, read_data)
    def handle(self, index, data):
        return index, data

class CsvInputHandler(BaseInputHandler):
    def __init__(self, stream):
        super(CsvInputHandler, self).__init__(csv.DictReader(stream))

class JsonInputHandler(BaseInputHandler):
    def handle(self, index, data):
        try:
            return index, json.loads(data)
        except ValueError, error:
            raise BadLine('line %d malformed: %s' % (index, error))


class BaseOutputHandler(BaseHandler):
    SUFFIX='OutputHandler'
    SEPARATOR=' '
    def __init__(self, keys):
        self.keys = keys
    def handle(self, index, indata):
        outdata = []
        for key in self.keys:
            try:
                value = unicode(indata[key]).encode('utf8')
            except KeyError:
                raise BadLine('missing key %s at line %d' % (key, index))
            self.append(outdata, index, key, value)
        return self.SEPARATOR.join(outdata)
    def append(self, outdata, index, key, value):
        raise NotImplementedError('%s must be subclassed' % (self.__class__.__name__,))

class KeyValueOutputHandler(BaseOutputHandler):
    SEPARATOR=","
    def append(self, outdata, index, key, value):
        outdata.append("%s=%s" % (key, value))

class SpacedOutputHandler(BaseOutputHandler):
    def append(self, outdata, index, key, value):
        outdata.append(value)

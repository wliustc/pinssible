import sys
import pycurl
import time
import zlib

class Test:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf

sys.stderr.write("Testing %s\n" % pycurl.version)

start_time = time.time()

url = 'http://www.dianping.com/shanghai'
url = "http://www.amazon.com/xa/dealcontent/v2/GetDealStatus?nocache=1426213473087"
data = '{"requestMetadata":{"marketplaceID":"ATVPDKIKX0DER","clientID":"goldbox","sessionID":"187-8170368-6201069","customerID":"A16U0JGOQDX82"},"dealTargets":[{"dealID":"0dbc1d74","itemIDs":null},{"dealID":"225e9679","itemIDs":null},{"dealID":"304062a7","itemIDs":null},{"dealID":"327fac6c","itemIDs":null},{"dealID":"34fad87e","itemIDs":null},{"dealID":"3b294e79","itemIDs":null},{"dealID":"63296719","itemIDs":null},{"dealID":"c9071f7c","itemIDs":null},{"dealID":"e6539878","itemIDs":null},{"dealID":"f95e242d","itemIDs":null}],"responseSize":"STATUS_ONLY","itemResponseSize":"NONE"}'
data = '{"requestMetadata":{"marketplaceID":"ATVPDKIKX0DER","clientID":"goldbox","sessionID":"187-8170368-6201069","customerID":"A16U0JGOQDX82"},"dealTargets":[{"dealID":"0dbc1d74","itemIDs":null},{"dealID":"225e9679","itemIDs":null},{"dealID":"304062a7","itemIDs":null},{"dealID":"327fac6c","itemIDs":null},{"dealID":"34fad87e","itemIDs":null},{"dealID":"3b294e79","itemIDs":null},{"dealID":"63296719","itemIDs":null},{"dealID":"c9071f7c","itemIDs":null},{"dealID":"e6539878","itemIDs":null},{"dealID":"f95e242d","itemIDs":null}],"responseSize":"STATUS_ONLY","itemResponseSize":"NONE"}'
#url = "https://dyn.keepa.com/service/deals/?user=4fa3ad183ad7ab70e60c91c8910bf81f27802e0189edd4af46be8491accd29b7&type=basic&domain=1&interval=2&merchant=1&category=0&start=96&perPage=24&exclude=0"
t = Test()
c = pycurl.Curl()
c.setopt(c.URL, url)

c.setopt(c.POSTFIELDS, data)

c.setopt(c.WRITEFUNCTION, t.body_callback)
c.perform()
end_time = time.time()
duration = end_time - start_time
print c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL)
c.close()

print 'pycurl takes %s seconds to get %s ' % (duration, url)

print 'lenth of the content is %d' % len(t.contents)

#contents = zlib.decompress(t.contents, 16+zlib.MAX_WBITS);
print(t.contents)
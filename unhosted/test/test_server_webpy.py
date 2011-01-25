import unittest

import time
import urllib2


class Test_Server_WebPy(unittest.TestCase):

    def setUp(self):
        self.host = "http://localhost:8080/unhosted"
        self.user = int(time.time())

    def test_shuffle(self):
        command = {"method": "GET",
                   "user": self.user,
                   "keyHash": "foo"
                   }
        data = {"protocol": "UJJP/0.2;KeyValue-0.2",
                "command": command}

        req = urllib2.Request(self.host, data)
        req.add_header('Referer', 'http://wabubi.ws/examples/')
        r = urllib2.urlopen(req)
        self.assertEqual(r.read(), )

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)


if __name__ == '__main__':
    unittest.main()
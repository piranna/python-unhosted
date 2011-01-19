# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

from twisted.trial import unittest

import unhosted
import unhosted.storage.dict
import unhosted.utils

class DictStorageTestCase(unittest.TestCase):

    def test_10_empty_dict(self):
        # Instance for testing
        storage = unhosted.storage.dict.DictStorage({})
        assert unhosted.IStorage.providedBy(storage)

        account = storage.account("userName", "userMail", "node", "app")
        account1 = storage.account("userName1", "userMail", "node", "app")
        assert unhosted.IAccount.providedBy(account)
        assert unhosted.IAccount.providedBy(account1)

        # Params required
        self.failUnlessRaises(TypeError, storage.get)
        self.failUnlessRaises(TypeError, storage.set)
        self.failUnlessRaises(TypeError, storage.has)

        # Get-set-has
        self.failIf(storage.has(account, "key"))
        storage.set(account, "key", "value", "sign")
        self.failUnless(storage.has(account, "key"))
        self.failUnlessEqual(storage.get(account, "key"), ("value", "sign"))
        self.failUnless(storage.has(account, "key"))
        self.failIf(storage.has(account1, "key"))
        self.failIf(storage.has(account, "key1"))
        self.failIf(storage.has(account1, "key1"))

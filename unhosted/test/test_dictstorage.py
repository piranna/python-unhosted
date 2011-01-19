# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

from twisted.trial import unittest

import unhosted
import unhosted.storage
import unhosted.utils

class Unhosted_0_2_TestCase(unittest.TestCase):

    def test_10_empty_dict(self):
        import unhosted
        import unhosted.storage

        # Instance for testing
        storage = unhosted.storage.DictStorage({})

        # Params required
        self.failUnlessRaises(TypeError, storage.get)
        self.failUnlessRaises(TypeError, storage.set)
        self.failUnlessRaises(TypeError, storage.has)

        # Get-set-has
        self.failIf(storage.has("account", "key"))
        storage.set("account", "key", "value", "sign")
        self.failUnless(storage.has("account", "key"))
        self.failUnlessEqual(storage.get("account", "key"), ("value", "sign"))
        self.failUnless(storage.has("account", "key"))
        self.failIf(storage.has("account1", "key"))
        self.failIf(storage.has("account", "key1"))
        self.failIf(storage.has("account1", "key1"))

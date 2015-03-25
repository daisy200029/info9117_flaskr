import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink( flaskr.app.config['DATABASE'] )

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here yet' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_multiple_login_logout(self):
        # Test admin login
        rv1 = self.login('admin', 'default')
        print("rv1", rv1)
        assert 'You were logged in' in rv1.data
        print ("rv1.data",rv1.data)

        rv3 = self.logout()
        print("rv3", rv3)
        assert 'You were logged out' in rv3.data
        print("rv3.data", rv3.data)


        # Test Jim login
        rv = self.login('jim', 'bean')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data

        # Test Spock login
        rv = self.login('spock', 'vulcan')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data


        # Test non-recognised users
        rv = self.login('adminx', 'default')

        assert 'Invalid username' in rv.data

        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv2 = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
			starttime='<2012.2.2>',
			endtime='<2012.2.6>'), follow_redirects=True)
        print("rv2",rv2)
        assert 'No entries here so far' not in rv2.data
        assert '&lt;Hello&gt;' in rv2.data
        assert '<strong>HTML</strong> allowed here' in rv2.data
        print("messages_rv2.data",rv2.data)
        self.logout()

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hihi>',
            text='<strong>HTML</strong> allowed here',
			starttime='<2012.2.2 23:00>',
			endtime='<2012.2.6 23:20>'), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hihi&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        self.logout()




        self.login('jim', 'bean')
        rv = self.app.post('/add', data=dict(
            title='<how are you>',
            text='<strong>HTML</strong> allowed here',
			starttime='<2014/5/4>',
			endtime='<2015/4/7>'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;how are you&gt; <span class=user> by jim' in rv.data
        self.logout()

        self.login('spock', 'vulcan')
        rv = self.app.post('/add', data=dict(
            title='<Happy>',
            text='<strong>HTML</strong> allowed here',
			starttime='<2014.5.4 12:00>',
			endtime='<2015.4.7 12:01>'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Happy&gt; <span class=user> by spock' in rv.data
        self.logout()





if __name__ == '__main__':
    unittest.main()



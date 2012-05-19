import urllib2
opener = urllib2.build_opener(urllib2.HTTPHandler)
#server = 'http://voteserver.herokuapp.com'
server = 'http://127.0.0.1:5000'

request = urllib2.Request(server + '/71f53486311cfe9b/register?fullname=brakobama&email=asdf@google.com', data='test')
request.add_header('Content-Type', 'text/plain')
request.get_method = lambda: 'PUT'
url = opener.open(request)


request = urllib2.Request(server + '/71f53486311cfe9b/my?title=vote1&text=weeeee&start_date=2012-04-17T13%3A07%3A31.887015&end_date=2012-04-17T13%3A07%3A31.887015')
request.add_header('Content-Type', 'text/plain')
request.get_method = lambda: 'PUT'
response = opener.open(request)

request = urllib2.Request(server + '/71f53486311cfe9b/fill_test_data')
request.add_header('Content-Type', 'text/plain')
request.get_method = lambda: 'PUT'
url = opener.open(request)

request = urllib2.Request(server + '/71f53486311cfe9b/fill_test_data')
request.add_header('Content-Type', 'text/plain')
request.get_method = lambda: 'PUT'
url = opener.open(request)

#request = urllib2.Request(server + '/71f53486311cfe9b/my/4/invite?users=5,7,')
#request.add_header('Content-Type', 'text/plain')
#request.get_method = lambda: 'PUT'
#url = opener.open(request)

request = urllib2.Request(server + '/71f53486311cfe9b/my/135/publish')
request.add_header('Content-Type', 'text/plain')
request.get_method = lambda: 'PUT'
response = opener.open(request)
print response.read()

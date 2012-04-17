import urllib2
opener = urllib2.build_opener(urllib2.HTTPHandler)

request = urllib2.Request('http://127.0.0.1:8080/register/00112233?fullname=brakobama&email=asdf@google.com', data='test')
request.add_header('Content-Type', 'text/plain')
request.get_method = lambda: 'PUT'
url = opener.open(request)


request = urllib2.Request('http://127.0.0.1:8080/00112233/my?title=vote1&text=weeeee&publication_date=2012-04-17T13%3A07%3A31.887015&start_date=2012-04-17T13%3A07%3A31.887015&end_date=2012-04-17T13%3A07%3A31.887015&results_date=2012-04-17T13%3A07%3A31.887015')
request.add_header('Content-Type', 'text/plain')
request.get_method = lambda: 'PUT'
url = opener.open(request)

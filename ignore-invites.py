# -*- coding: utf-8 -*-

import sys, requests, json, codecs, time
from getpass import getpass
from bs4 import BeautifulSoup

# Create session
session = requests.session()
headers = {'User-Agent': ''}        # Yes, this is all the headers you need

# Log in
email = raw_input('Enter email: ')
password = getpass('Enter password: ')
data = {'email': email, 'password': password}
response = session.post('https://www.zhihu.com/login/email', headers = headers, data = data)
if response.status_code == 200 and response.json()['msg'] == u'登陆成功':
    print 'Login successful!'
else:
    print 'Login failed!'
    sys.exit(1)

# Load the invitations page by page and ignore them
while True:
    # Load one page of invitations
    # Because the server may occasionally return errors, repeat until success
    while True:
        response = session.get('https://www.zhihu.com/question/invited', headers = headers)
        if response.status_code == 200: break

    # Parse page
    soup = BeautifulSoup(response.text)

    # See how many invitations are left
    count = int(soup.find('div', {'class': 'zm-invite-container'}).span.text[4:-1])
    if count == 0:
        print '\nAll invitations have been ignored. Yay!'
        break
    print '\nNow you have %d invitation%s.' % (count, '' if count == 1 else 's')

    # Find two values that are useful later:
    #   uid: a hash code identifying the user
    #   xsrf: a hash code confirming that you are logged in
    uid = json.loads(soup.find('script', {'data-name': 'ga_vars'}).text)['user_hash']
    xsrf = soup.find('input', {'name': '_xsrf'})['value']

    # Get the list of invitations on the current page
    invites = soup.findAll('div', {'class': 'zm-invite-item'})

    # Examine each invitation
    for invite in invites:
        # Parse invitation
        qid = invite.find('a', {'name': 'ignore'})['data-qid']
        title = invite.find('a', {'class': 'question_link'}).text.strip()
        inviter = invite.find('a', {'class': 'zg-link'}).text.strip()
        inviter_link = invite.find('a', {'class': 'zg-link'})['href']

        # Save invitation in log file
        with codecs.open('log.htm', 'a', 'utf-8') as f:
            f.write(u'<p><a target=_blank href="%s">%s</a> 邀请你回答 <a target=_blank href="https://www.zhihu.com/question/%s">%s</a></p>\n' %
                    (inviter_link, inviter, qid, title))

        # Prepare the data for the POST request to ignore the invitation
        # Fields:
        #   op: short for operation, "pass" means "ignore"
        #   qid: the ID of the question
        #   uid and xsrf: as explained above
        data = {'op': 'pass', 'qid': qid, 'uid': uid, '_xsrf': xsrf}

        # Ignore invitation
        response = session.post('https://www.zhihu.com/question/askpeople', headers = headers, data = data)
        status = 'Ignored' if response.status_code == 200 else 'Failed '
        try:
            print '%s: %s | %s | %s' % (status, qid, inviter, title)
        except UnicodeEncodeError:
            print '%s: %s | [Contains special characters]' % (status, qid)

        # Sleep 5 seconds, so you don't get your account frozen for accessing too frequently
        time.sleep(5)

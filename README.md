# zhihu-ignore-invites

This script will ignore all your invitations on [zhihu.com](https://zhihu.com), so you don't have to ignore them one by one.

The script is written in Python 2. You need to have [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) installed first.

Upon running the script, you will be prompted for your email and password. Then, it will start ignoring invitations at a speed of one per five seconds. I know this is slow, but going faster may result in your account getting suspended.

Note that ignored invitations cannot be restored! However, links to the questions will be dumped to the log file ```log.htm```, in case you may want to browse them later.

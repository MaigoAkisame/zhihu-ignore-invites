# zhihu-ignore-invites

**Warning: Do not use the script for the moment! I just found out that my account was frozen for too frequent accesses after ignoring a few hundred questions.**

This script will ignore all your invitations on [zhihu.com](https://zhihu.com), so you don't have to ignore them one by one.

The script is written in Python 2. You need to have [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) installed first.

Upon running the script, you will be prompted for your email and password. Then, it will start ignoring invitations at a speed of around 2 invitations per second.

The script really ignores all invitations! In case you may find some questions that you do want to answer, it is recommended that you pipe the output of the script to a file for record, like this:
```
python ignore-invites.py | tee ignore-invites.log
```

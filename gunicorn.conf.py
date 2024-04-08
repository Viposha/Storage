access_log_format = '%(t)s [%({x-forwarded-for}i)s %(M)sms] "%(m)s %(U)s?%(q)s" %(s)s %(b)s'
preload_app = True
timeout = 60
bind = '157.230.112.86:8000'
workers = 1
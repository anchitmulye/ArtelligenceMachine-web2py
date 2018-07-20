
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")


configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    
    db = DAL('google:datastore+ndb')
   
    session.connect(request, response, db=db)
 
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''


auth = Auth(db, host_names=configuration.get('host.names'))


auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)


mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com'
mail.settings.sender = '*******'
mail.settings.login = '*******:*******'
mail.settings.tls = 587
mail.settings.ssl = 465


auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')


response.google_analytics_id = configuration.get('google.analytics_id')


if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configure.get('heartbeat'))


db.define_table('contact',
                Field('name', requires=IS_NOT_EMPTY()),
                Field('email',requires=IS_NOT_EMPTY()),
                Field('subject' ),
                Field('post', type ='text'),
                Field('status', default ='Not send' , writeable = True)
                )

#main controller
#

def index():
    form = SQLFORM(db.contact, submit_button='Send Message',formstyle='table2cols',ignore_rw=True).process()
    if form.accepted:
        for row in db(db.contact.status != 'Email Sent').select(db.contact.email,db.contact.name):
            name = str(row.name)
            mail.send(to=[row.email], subject='noreply', message=('Hello '+name+'!\n\nThank you for contacting us. We will reach to you shortly.\n\n\n'+'This is computer generated email please do not reply.\nArtelligence Machine\nhttps://artelligencemachine.ml'))
    else:
        pass
    db(db.contact.status == '').update(status='Email Sent')
    return locals()


@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})


@auth.requires_membership('admin') 
def grid():
    response.view = 'generic.html' 
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

def wiki():
    auth.wikimenu() 
    return auth.wiki() 

def user():
   
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

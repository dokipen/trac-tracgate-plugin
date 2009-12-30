from email.utils import parseaddr

def find_sid_by_email(env, email):
    """
    Lookup user sid by email address.  If it isn't found, returns address 
    part of email.
    """
    _, addr = parseaddr(email)
    db = env.get_db_cnx()
    cursor = db.cursor()
    cursor.execute("""
        SELECT sid
          FROM session_attribute
         WHERE name = 'email'
           AND value = %s
    """, (addr,))
    sid = cursor.fetchone()
    if sid and len(sid) > 0:
        return sid[0]
    else:
        return addr

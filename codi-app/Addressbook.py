import sqlite3
import CodiStatus

def contactNameForNumber(number):
    for c in CodiStatus.Contacts:
        if c[2] == number:
            return c[1]
    return 'Unknown'


def refreshContacts():
    CodiStatus.Contacts = []

    try:
        conn = sqlite3.connect('/home/cosmo/.local/share/evolution/addressbook/system/contacts.db')
        c = conn.cursor()
        statement = 'select * from folder_id'
        contacts = c.execute(statement)
        for contact in contacts:
            id = ''
            name = ''
            numbers = []
            addContact = True
            for l in contact[15].split('\n'):
                if l.startswith('X-DELETED-AT:'):
                    addContact = False
                if l.startswith('FN:'):
                    name = l[3:]
                if l.startswith('UID:'):
                    id = l[4:].strip()
                if l.startswith('TEL;'):
                    tokens = l.split(';')
                    for t in tokens:
                        if t.startswith('TYPE='):
                            t = t[5:]
                            sep = t.index(':')
                            phType = t[0:sep].strip()
                            phNumber = t[sep+1:].strip()
                            numbers += [(phType, phNumber)]

            if name != '' and addContact:
                for n in numbers:
                    CodiStatus.Contacts += [(id, name, n[1])]

        conn.commit()
        c.close()
        conn.close()
    except Exception as e:
        print('Exception:', e)

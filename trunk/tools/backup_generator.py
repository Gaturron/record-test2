#backup generator
import os, subprocess, zipfile
from time import gmtime, strftime

# variables
#page_dir = '/home/fer/recordtest'
page_dir = '/home/fbugni/record-page'
#backup_dir = '/home/fer/recordtest-backup'
backup_dir = '/home/fbugni/record-page-backup'

time = strftime("%Y-%m-%d_%H:%M:%S", gmtime())

#create a tmp directory
tmp_dir = r'tmp_dir-'+time

try:
    if not os.path.exists(backup_dir+'/'+tmp_dir): os.makedirs(backup_dir+'/'+tmp_dir)
except OSError:
    print 'Failed creating tmp folder'

#postgres dump
database = 'django_db'
username = 'django_login'
password = '1234'
filename_dumpsql = 'dump.sql'
command = 'export PGPASSWORD=%s\npg_dump %s -U %s --file="%s" -h localhost' % (password, database, username, backup_dir+'/'+tmp_dir+'/'+filename_dumpsql)
try:
    os.system(command)
except OSError:
    print 'Failed dumping de database'

#export json
filename_dumpjson = 'dump.json'
command = page_dir+'/manage.py dumpdata > "%s"' % (backup_dir+'/'+tmp_dir+'/'+filename_dumpjson)
try:
    os.system(command)
except OSError:
    print 'Failed exporting to json'

#rsync audios
audios_dir = r'audios'
try:
    command = 'rsync -a --backup --suffix .`date +"%Y-%m-%d_%H:%M"` '+page_dir+'/media/audios/*.wav '+backup_dir+'/'+audios_dir+'/'
    os.system(command)
except OSError:
    print 'Failed copying audios'

#create zip file
def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

zip = zipfile.ZipFile(backup_dir+'/database/Backup-'+time+'.zip', 'w')
zipdir('./'+tmp_dir+'/', zip)
zip.close()

#delete tmp directory
try:
    command = ' rm -rf '+backup_dir+'/'+tmp_dir
    os.system(command)
except OSError:
    print 'Failed to delete tmp directory'
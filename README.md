REBUILD AND CLEAN DB
MAKE DUMP
pg_dump -Fc bitcore -h bitcore-prod-backup.ckqzildhfiwx.eu-central-1.rds.amazonaws.com -U bitcore_admin > database.bak
Cyberpunk2077

RESTORE DUMP
pg_restore -h bitcore-production.ckqzildhfiwx.eu-central-1.rds.amazonaws.com -U bitcore_admin -d bitcore -1 database.bak
Ikkitousen!2019

add colum "name" to django_content_type

delete migrations on db

python3 manage.py migrate --fake-initial

copy all publication and calendar images flattened out in the media folder
(script to flatten the images?)

is_staff to all writes so they can be picked
# BitcoreBackend
# BitcoreBackend

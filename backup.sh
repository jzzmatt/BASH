#!/bin/bash

TEMP_BKP_FOLDER="Backup/"

#DISPLAY USAGE SCRIPT
if [[ "${#}" -lt 1 ]]
then
    echo "Usage: ${0} [SRC FOLDER] [DESTINATION PATH]"
    exit 1
fi

#SYNC SOURCE FOLDER TO BACKUP FOLDER
if [[ -d "${1}" ]]
then
    rsync -ahvzP "${1}" "${2}${TEMP_BKP_FOLDER}"
else
    echo "Make sure the Source Folder Exist"
    exit 1
fi
#COMPRESS EXISTING BACKUP FOLDER
if [[ "${?}" != 1 ]]

then
    tar -cvzf "BACKUP.tar.gz" "${2}${TEMP_BKP_FOLDER}"
    rm -rf "${2}${TEMP_BKP_FOLDER}"
fi

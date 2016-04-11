"""

Copyright 2015 Stefano Terna

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import os, shutil, logging, tarfile, sys

from iottly.settings import settings

logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s [%(levelname)s] (%(processName)-9s) %(message)s',)


agentpath, filename = os.path.split(sys.argv[0])

userpackagepath = 'userpackage/'

# check that iottly service is not running


# check if a new fw is available
logging.info('Searching for firmware archive in {} ...'.format(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR))
if os.path.exists(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR):
    fws = os.listdir(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR)
else:
    logging.info('No firmware dir found. Exiting installer ...')
    quit()

fwfilename = None

if len(fws) > 1:
    raise Exception('Found more than 1 firmware available. Something weird happened here.')
elif len(fws) == 0:
    logging.info('No firmware found. Exiting installer ...')
    quit()
elif len(fws) == 1:
    fwfilename = os.path.join(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR, fws[0])
    logging.info('Found firmware: \n{}.\nInstalling.'.format(fwfilename))

if fwfilename:
    try:
        # remove old fw
        if os.path.exists(userpackagepath):
            logging.info('Removing old package ...')
            shutil.rmtree(userpackagepath)

        # untar new fw into proper destination
        logging.info('Extracting archive ...')
        with tarfile.open(fwfilename) as tar:
            tar.extractall(agentpath)
        logging.info('Installation successful!')
    except Exception as e:
        logging.error(e)
    finally:
        #always remove firmware fwfilename
        logging.info('Removing archive ...')
        os.remove(fwfilename)

        logging.info('Done!')
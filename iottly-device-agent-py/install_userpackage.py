import os, shutil, logging, tarfile

from iottly.settings import settings

logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s [%(levelname)s] (%(processName)-9s) %(message)s',)

userpackagepath = 'userpackage/'

# check that iottly service is not running


# check if a new fw is available
logging.info('Searching for firmware archive in {} ...'.format(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR))
fws = os.listdir(settings.IOTTLY_USERPACKAGE_UPLOAD_DIR)
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
            tar.extractall()
        logging.info('Installation successful!')
    except Exception as e:
        logging.error(e)
    finally:
        #always remove firmware fwfilename
        logging.info('Removing archive ...')
        os.remove(fwfilename)

        logging.info('Done!')
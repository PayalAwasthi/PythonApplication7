'''
Created on Oct 13, 2016

@author: savarshn
'''

import config
import thor.commonutils.basicutils as basicThorUtils
import thor.commonutils.installerutils as installUtils
import thor.commonutils.loggerUtils as loggerUtils
import thor.commonutils.screencapture as screenCapture
import argparse


if __name__=='__main__':
    '''
    In this workflow Thor will be installed and uninstalled multiple times
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--buildNumber')
    parser.add_argument('--branchNumber')
    parser.add_argument('--count')
    args = parser.parse_args()
    branch=args.branchNumber
    buildno=args.buildNumber
    count=args.count
    
    logger = loggerUtils.Logger()
    config.screenShotObj=screenCapture.ScreenCapture()
    logURLList=[]
    failCount=0
    try:
        for i in range(count):
            config.logObj.info('*************** Running for '+str(i+1)+' times')
            if installUtils.installThorUsingLBS(branch, buildno):
                config.logObj.info("Thor installed")    
            else:
                config.logObj.error("Thor not installed properly")
                failCount+=1
            url=basicThorUtils.uploadLogsToServer()
            logURLList.append(url)
            installUtils.uninstallThor()
    except Exception,e:
        config.logObj.critical(str(e))
    url=basicThorUtils.uploadLogsToServer()
    logURLList.append(url)
    config.logObj.info('Log file urls: '+str(logURLList))
    config.logObj.info(str(failCount)+' failed out of '+str(count))
    logger.uploadLogFile('ThorInstallUninstall',branch,buildno)
    
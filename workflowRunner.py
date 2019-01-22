'''
Created on Jul 21, 2015

@author: sarthak
'''
import argparse, sys, os, time, socket, subprocess

import config
import thor.uiutils.nativeutils.native as native
import thor.commonutils.RDCUtil as rdcUtil
import thor.commonutils.accountpoolservice as accountService
import thor.commonutils.basicutils as basicThorUtils
import thor.commonutils.dataDumpUtil as dataDumpUtil
import thor.commonutils.installerutils as installUtils
import thor.commonutils.loggerUtils as loggerUtils
import thor.commonutils.mailutils as mailUtils
import thor.commonutils.screencapture as screenCapture
import thor.resultreporter.htmlgenerator as htmlGenerator
import thor.resultreporter.machineinfo as machineInfo
import thor.resultreporter.resultdict as resultReporter
import thor.uiutils.seleniumutils as utils
import workflow.acceptanceworkflows.filesAcceptance as filesAcceptance
import workflow.acceptanceworkflows.fontsAcceptance as fontsAcceptance
import workflow.acceptanceworkflows.marketacceptance as marketAcceptance
import workflow.appsworkflow.InstallWorkflow as installWorkflow
import workflow.appsworkflow.appsRCWorkflow as appsRCWorkflow
import workflow.appsworkflow.appsRCWorkflow_2 as appsRCWorkflow2
import workflow.appsworkflow.appsAutoUpdateWorkflow as appsAutoUpdateWorkflow
import workflow.appsworkflow.ASURCWorkflow as ASURCWorkflow
import workflow.appsworkflow.fullAppUpdateWorkflowV2 as fullAppUpdateWorkflow
import workflow.appsworkflow.updateAllWorkflow as updateAllWorkflow
import workflow.appsworkflow.HDEngineRCWorkflow as HDEngineRCWorkflow
import workflow.ccLaunchworkflow.ccLaunch as ccLaunch
import workflow.filesystemvalidator.thorfilesystemvalidator as thorFileSystemValidator
import workflow.idsworkflow.idVerifier as idVerifier
import workflow.sanity.sanitybehance as sanityBehance
import workflow.sanity.sanitycontainer as sanityContainer
import workflow.sanity.sanityfiles as sanityFiles
import workflow.sanity.sanityfonts as sanityFonts
import workflow.sanity.sanityhelper as sanityHelper
import workflow.sanity.sanity_learn as sanityLearn
import workflow.sanity.sanityasync as sanityAsync
import workflow.sanity.sanityunc as sanityUnc
from workflow.sanity.sanitymarket import sanityMarket
import workflow.sanity.sanitystocks as sanityStocks
import workflow.sanity.SanityAppsV2 as sanityAppsV2
import workflow.selfupdateworkflow.selfUpdate as selfUpdate
import workflow.selfupdateworkflow.selfUpdateCCNotRunning as selfUpdateCCNotRunning
import workflow.selfupdateworkflow.selfUpdateCCSignedinRunning as selfUpdateCCSignedinRunning
import workflow.selfupdateworkflow.selfUpdateSignoutSignin as selfUpdateSignoutSignin
import workflow.selfupdateworkflow.selfUpdateYetNewerVersion as selfUpdateYetNewerVersion
import workflow.appsworkflow.ccAppsLoadPerformance as ccAppsLoadPerformance
from thor.commonutils import stringsHandler, ftputils
from workflow.appsworkflow import hdProductsPerformanceWorkflow
from workflow.appsworkflow import latestHDProductsInstallWorkflow
from workflow.appsworkflow import ribsProductsPerformanceWorkflow
from workflow.appsworkflow import latestProductInstallWorkflow
from workflow.appsworkflow import singleAppInstallWorkflow
from workflow.appsworkflow import dirtyMachineWorkflow
from distutils.version import StrictVersion
import workflow.genericworkflows.buildDeassembler as buildDeassembler
import workflow.genericworkflows.mergeAutomationCoverageFiles as mergeAutomationCoverageFiles
from workflow.acceptanceworkflows import appsAcceptance
import workflow.appsworkflow.productInstallUninstallWorkflow as productInstallUninstallWorkflow


if __name__ == '__main__':
    
    '''
    arguments from jenkins job
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--buildNumber')
    parser.add_argument('--branchNumber')
    parser.add_argument('--workflowName')
    parser.add_argument("--subscription")
    
    ''' Optional arguments'''
    parser.add_argument('--environment')
    parser.add_argument('--usePassedEnvironment')
    parser.add_argument("--idtype")
    parser.add_argument("--ffcStack")
    parser.add_argument("--iteration")
    parser.add_argument("--mode")
    parser.add_argument("--locale")
    parser.add_argument("--lbsLocation")
    parser.add_argument("--useLegacyLBS")
    parser.add_argument("--useNonElevatedACC")
    parser.add_argument('--ASUbuildNumber')
    parser.add_argument('--ASUbranchNumber')    
    parser.add_argument('--CCApps')    

    '''This argument --updateFes is needed when we need to host fes.xml to local system and make necessary changes
    Possible values could be --updateFes=ngl:enabled, ngl:disabled, hidePanel:learn etc'''
    parser.add_argument("--updateFes")
    
    '''
        DO NOT USE ADDITIONAL ARGUMENTS. USE extras with &&& separator for myltiple values. key:value or key:comma-separated-values
        e.g extras = "iteration===1"
        e.g extras = "products===Photoshop CC,Illustrator &&& iteration===1" 
    '''
    parser.add_argument('--extras')
    
    args = parser.parse_args()
    
    environment=args.environment
    usePassedEnvironment=args.usePassedEnvironment
    branch=args.branchNumber
    buildno=args.buildNumber
    workflowid=args.workflowName
    subscription=args.subscription
    idtype=args.idtype
    ffcStack=args.ffcStack
    mode=args.mode
    lbsLocation = args.lbsLocation
    useLegacyLBS = args.useLegacyLBS
    useNonElevatedACC = args.useNonElevatedACC
    ASUbranch=args.ASUbranchNumber
    ASUbuildno=args.ASUbuildNumber    
    locale=args.locale
    iteration = args.iteration
    extras = args.extras
    CCApps = args.CCApps
    
    ''' 
        mode is an argument to be given for running Automation jobs
        mode should be "debug" at the time of testing the workflows
        mode should be "run" at the time of running the workflows 
    '''
    if mode==None:
        mode="debug"
    
    ''' If LBS location is given, override default config value
        Possible values could be localserver, ftp, web
    '''
    if lbsLocation:
        config.LBS_LOCATION = lbsLocation
        
    ''' If useLegacyLBS is True, use legacy lbs (not Kaizen installer for Thor).
        Otherwise, use Kaizen installer for Thor.
    '''
    if useLegacyLBS == 'true':
        config.USE_LEGACY_LBS = True
    elif useLegacyLBS == 'false':
        config.USE_LEGACY_LBS = False
    else:
        config.USE_LEGACY_LBS = False
        
    if usePassedEnvironment == 'true':
        config.usePassedEnvironment = True
    elif usePassedEnvironment == 'false':
        config.usePassedEnvironment = False
    else:
        config.usePassedEnvironment = False
        
    if useNonElevatedACC == 'true':
        config.useNonElevatedACC = True
        
        #TODO: To explore other options
        UserProfilePath = "C:\\Users\\stduser\\"  
        
        #TODO: Temporary commit until a better solution is implemented
        config.AAM_UPDATER_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Adobe", "AAMUpdater","1.0")
        config.DLM_LOG_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Temp", "CreativeCloud","ACC","AdobeDownload")
        config.DLM_LOG_FILE_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Temp", "CreativeCloud","ACC","AdobeDownload","DLM.log")
        config.OOBETempDirectory=os.path.join(UserProfilePath,"AppData","Local","Adobe","OOBE")
        config.PII_PATH = os.path.join(UserProfilePath,"AppData", "Local", "Adobe","PII","com.adobe.pii.prefs")
        config.DESKTOPPATH=os.path.join(UserProfilePath,"Desktop")
        config.ThorCreativeCloudFilesFolder=os.path.join(UserProfilePath, 'Creative Cloud Files')
        config.ACC_LOG_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Temp",'CreativeCloud','ACC',"ACC.log")
        config.PDAPP_LOG_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Temp","CreativeCloud","ACC.log")
        
        #TODO: Revert this change. Temporarily modify mailing list only for testing Non elevated scenario
        config.MAIL_LIST_AUTO = ['rewari@adobe.com']
        config.MAIL_LIST_LEAD = ['rewari@adobe.com']
        config.MAIL_LIST_MANAGERS = ['rewari@adobe.com']

    elif useNonElevatedACC == 'false':
        config.useNonElevatedACC = False
    else:
        config.useNonElevatedACC = False
    
    #Storing fes.xml update info in config
    if args.updateFes:
        config.UPDATE_FES = args.updateFes
    
    config.environment=environment
    
    config.usePassedEnvironment=usePassedEnvironment
    
    if not config.usePassedEnvironment:
        if ".s" in buildno:
            config.environment = "stage"
        else:
            config.environment = "prod"

    config.branch=branch
    config.buildno=buildno
    config.subscription=subscription
    config.idtype=idtype
    config.ffcStack=ffcStack
    config.locale=locale
    #workflowid == "ProductInstallUninstallWorkflow"
    #config.workflowid=workflowid 
    config.workflowid="LatestProductInstallWorkflow"

    config.ASUBranch = ASUbranch
    config.ASUBuildno = ASUbuildno
    config.CCApps = CCApps
    config.mode=mode
    if iteration:
        config.iteration = int(iteration)
    
    ''' Load string data '''
    config.string = stringsHandler.getData(config.locale)
    
    #initialize logger
    logger = loggerUtils.Logger()
    config.logObj.info('Logger initiated')
    
    if extras:
        if stringsHandler.parseExtras(extras):
            config.logObj.info('Successfully parsed extras - ' + str(config.extras))
        else:
            config.logObj.critical("FAILED to parse extras. Invalid format - " + str(extras))
            htmlGenerator.HtmlReporter().generateSimpleHTML("Invalid format for extras - " + str(extras),"ERROR_MAIL")
            sys.exit(1)
    
    #Display list of running processes and raise alert if Explorer.exe is in system mode

    basicThorUtils.alertExplorerSystemMode()
    if config.mode == "run":

        #Disable RDCM call as our new Openstack RDUtility is workflow independant
#         rdcObj = rdcUtil.RDCUtil()
#         rdcObj.updateDB('1')
        try:
            #Check if Automation started indicator file is present
            if not os.path.exists(config.AutomationStartedCheckFilePath):
                #Machine is clean, Add Automation started indicator
                config.logObj.info("Machine is in clean state")
                f=open(os.path.normpath(config.AutomationStartedCheckFilePath),'w+')
                f.close()
            else:
                #Machine is not clean, send mail alert and exit workflow with failure
                config.logObj.critical("Machine is not in clean state. Sending mail and Exiting....")
                htmlGenerator.HtmlReporter().generateSimpleHTML("Automation Job not started. Machine is not in clean state.","ERROR_MAIL")
                mailUtils.sendMail(config.MAIL_LIST_AUTO, "Machine revert failed : " + workflowid+" | ACC "+config.branch+" | Build# "+config.buildno+" | "+ machineInfo.machineName() +" | Environment: "+config.environment+" | ID: "+config.subscription, "Machine with IP : " + socket.gethostbyname(socket.gethostname()) + " is not in clean state, stopping execution of workflowRunner.py. Re-trigger from https://thor-automation.ci.corp.adobe.com:12001/ ", config.MAIL_ID_THORQE)
                time.sleep(20)
                sys.exit(1)
            
            if os.name =='nt':
                #Check for active remote desktop connection
                RD_info = subprocess.Popen('netstat -n | find ":3389 "', shell = True , stdout = subprocess.PIPE).stdout.read()

                if not RD_info or RD_info in [None, ""," "]:
                    htmlGenerator.HtmlReporter().generateSimpleHTML("Automation Job not started. No Remote Desktop connection detected.","ERROR_MAIL")
                    config.logObj.critical("No Remote Desktop connection detected. Job info : "+ workflowid+" | ACC "+config.branch+" | Build# "+config.buildno+" | "+ machineInfo.machineName() +" | Environment: "+config.environment+" | ID: "+config.subscription)
                    mailUtils.sendMail(config.MAIL_LIST_AUTO, "No Remote Desktop connection detected : " + workflowid+" | ACC "+config.branch+" | Build# "+config.buildno+" | "+ machineInfo.machineName() +" | Environment: "+config.environment+" | ID: "+config.subscription, "Machine with IP : " + socket.gethostbyname(socket.gethostname()) + " is not connected with Remote Desktop, stopping execution of workflowRunner.py. Re-trigger from https://thor-automation.ci.corp.adobe.com:12001/ ", config.MAIL_ID_THORQE)
                    time.sleep(20)
                    sys.exit(1)                
                else:
                    config.logObj.info("Remote desktop connection info : " + str(RD_info))
        
        except Exception,e:
            config.logObj.info("Exception occurred in pre-workflow validation")    

        #Data dump util initialisation
        config.dashboardDb = dataDumpUtil.DataDumpUtils()
        
    if config.idtype==None:
        config.idtype='Type1'
        
    try:
        if os.name=='nt' and mode=="run":
            native.startMonitoringCrashReporterDialog()
    except Exception,e:
        config.logObj.critical("Error in starting Monitoring of Crash Reporter dialog" + str(e))
    
    try:
        workflowRunnerExecutionStatus=True
        
        ''' Disabling memory usage mail functionality for CEF process
        threadObj = MemoryCheckerThread.MemoryCheckerThread(600)
        '''
        
        if ".s" in config.buildno and workflowid in ["ThorFileSystemValidatorSanityWorkflow", "ThorFileSystemValidatorUpdateWorkflow", "ThorUpdateYetNewerVersionWorkflow"]:
            config.logObj.info("Not running job on .s branch")
            htmlGenerator.HtmlReporter().generateSimpleHTML("Not running job on .s branch","ERROR_MAIL")
            sys.exit(1)
            
            
        #TODO: Discuss these checks for usePassedEnvironment.
        
        #For Stage environment, running job only on .s build
        elif config.environment == "stage" and ".s" not in config.buildno:
            config.logObj.info("Not running job as the environment is stage but the build is not '.s'.")
            htmlGenerator.HtmlReporter().generateSimpleHTML("Not running job on Stage as the build is not .s","ERROR_MAIL")
            sys.exit(1)
        #For Prod environment, running job only on non-*.s build
        elif config.environment == "prod" and ".s" in config.buildno:
            config.logObj.info("Not running job for this configuration - Environment - prod, Build - .s")
            htmlGenerator.HtmlReporter().generateSimpleHTML("Not running job for this configuration - Environment - prod, Build - .s", "ERROR_MAIL")
            sys.exit(1)
        
        #Download coverage file for Instrumented build
        if config.LBS_LOCATION.lower() == 'instrumented':
            basicThorUtils.downloadCoverageFileForInstrumentedBuild()
            
        #Workflow to deassemble build files and upload to FTP
        if workflowid=="BuildFilesDeassembler":
            buildDeassemblerObj= buildDeassembler.BuildFilesDeassembler(config.branch, config.buildno)
            buildDeassemblerObj.start()
            htmlGenerator.HtmlReporter().generateSimpleHTML("Execution over for deassembling build files.", "")
            sys.exit(1)
        
        #Workflow to Merge Automation Coverage Files
        if workflowid=="MergeAutomationCoverageFiles":
            mergeObj = mergeAutomationCoverageFiles.AutomationCoverage()
            mergeObj.mergeCovFiles()
            sys.exit(1)
        
        if config.subscription:
            userId=accountService.getIdFromService(config.subscription,config.environment,config.idtype)
            config.adobeid=userId[0]
            config.adobeidPass=userId[1]
        
        if not config.adobeid:
            config.logObj.info('No id is available in pool, exiting...')
            htmlGenerator.HtmlReporter().generateSimpleHTML("No id is available in pool","ERROR_MAIL")
            sys.exit(1)
        config.logObj.info('Adobe id used:' + str(config.adobeid))
        
        if workflowid in ["ThorFileSystemValidatorSanityWorkflow", "ThorFileSystemValidatorUpdateWorkflow"]:
            thorFileSystemValidatorObj=thorFileSystemValidator.ThorFileSystemValidator(workflowid)
            TFSVStatus=thorFileSystemValidatorObj.ThorFileSystemValidatorWorkflow()
            if config.adobeid:
                accountService.freeId(config.adobeid)
            if TFSVStatus:
                sys.exit(0)
            else:
                sys.exit(1)
            
        if config.ffcStack=="ffc-green-stack":
            basicThorUtils.updateFFCStackInHostsFile("green")
        elif config.ffcStack=="ffc-blue-stack":
            basicThorUtils.updateFFCStackInHostsFile("blue")
        
        if workflowid not in ['ThorPerformanceWorkflow']:
            basicThorUtils.setDetailedLog()
        
        config.screenShotObj=screenCapture.ScreenCapture()
        config.resultsObj=resultReporter.ResultDict(config.branch,config.buildno,config.environment,config.subscription)

        if workflowid not in ["ASURCWorkflow", "DirtyMachineWorkflow","ThorUpdateWorkflow","ThorUpdateHopWorkflow","ThorUpdateSignoutSigninWorkflow","ThorUpdateCCSignedinRunningWorkflow","ThorUpdateCCNotRunningWorkflow","ThorUpdateYetNewerVersionWorkflow"]:
   
            if not config.USE_LEGACY_LBS and StrictVersion(config.branch) >= StrictVersion('4.6'):
                config.logObj.info("Installing Thor by Kaizen")
                #Use 32 bit for mac
                if os.name != 'nt':
                    os.system("echo tester | sudo -S defaults write com.apple.versioner.python Prefer-32-Bit -bool yes")
                    time.sleep(5)
                              
                lbs_install_status = installUtils.installThorUsingKaizen(config.branch, config.buildno, config.LBS_LOCATION)
            else:
                config.logObj.info("Installing Thor by LBS")
                lbs_install_status = installUtils.installThorUsingLBS(config.branch, config.buildno, config.LBS_LOCATION)
                  
                          
            if not lbs_install_status:
                config.logObj.error('ERROR: Problem installing Thor build')
                basicThorUtils.uploadLogsToServer()
                if config.adobeid:
                    accountService.freeId(config.adobeid)
                config.screenShotObj.captureScreen()
                raise Exception('ERROR: Could not install Thor')
                          
                              
            if config.environment=="stage":
                config.screenShotObj.captureScreen()
                config.logObj.info("Applying Redirection for Stage Environment")
                basicThorUtils.applyRedirection()
                config.screenShotObj.captureScreen()
               
            basicThorUtils.launchCreativeCloud()
              
              
      
            config.seleniumObj=utils.SeleniumUtils()
         
            #Display list of running processes and raise alert if Explorer.exe is in system mode
            basicThorUtils.alertExplorerSystemMode()
             
        resultId=""

        if workflowid=="IdsWorkflow":
            idVerifierObj=idVerifier.idVerify(workflowid)
            idVerifierObj.idVerifyWorkflow()

        if workflowid=="LatestProductInstallWorkflow":
            latestProductInstallWorkflowObj = latestProductInstallWorkflow.LatestProductInstallWorkflow(workflowid)
            latestProductInstallWorkflowObj.workflowLatestProductInstall()
            ''' Commenting the verification for product launch because of AAM sign out screen appears on launching products '''
            #latestProductInstallWorkflowObj.verifyProductLaunch()
            
        if workflowid=='LatestHDProductsInstallWorkflow':
            latestHDProductsInstallWorkflowObj = latestHDProductsInstallWorkflow.LatestHDProductsInstallWorkflow(workflowid)
            latestHDProductsInstallWorkflowObj.workflowLatestHdProductInstall()
            
        if workflowid=='HDProductsPerformanceWorkflow':
            resultId="HD"
            config.resultsObj=resultReporter.PerformanceResultDict(config.branch,config.buildno,config.environment,config.subscription)
            hdProductsPerformanceWorkflowObj = hdProductsPerformanceWorkflow.HDProductsPerformanceWorkflow(
                
                
                
                
                
                
                
                
                
                )
            hdProductsPerformanceWorkflowObj.workflowHDProductsInstallAndPerformance()
        
        if workflowid=='RIBSProductsPerformanceWorkflow':
            resultId="RIBS"
            config.resultsObj=resultReporter.PerformanceResultDict(config.branch,config.buildno,config.environment,config.subscription)
            ribsProductsPerformanceWorkflowObj = ribsProductsPerformanceWorkflow.RIBSProductsPerformanceWorkflow(workflowid)
            ribsProductsPerformanceWorkflowObj.workflowRibsProductsInstallAndPerformance()
            
        if workflowid=='ThorPerformanceWorkflow':
            resultId="CCLAUNCH"
            config.resultsObj=resultReporter.PerformanceResultDict(config.branch,config.buildno,config.environment,config.subscription)
            ccLaunchObj=ccLaunch.ccLaunch(workflowid)
            ccLaunchObj.ccLaunchWorkflow()
            ccLaunchObj.containerObj.signout()
        
        if workflowid=="FullAppUpdatetruefalseWorkflow":
            if StrictVersion(config.branch) >= StrictVersion(config.REVAMPED_APPS_PANEL_BRANCH):
                fullAppUpdateObj = fullAppUpdateWorkflow.FullAppUpdate(workflowid)
            else:
                fullAppUpdateObj = installWorkflow.ProductInstall(workflowid)
            fullAppUpdateObj.workflowFullAppUpdatetruefalse()
            
        if workflowid=="FullAppUpdatefalsetrueWorkflow":
            if StrictVersion(config.branch) >= StrictVersion(config.REVAMPED_APPS_PANEL_BRANCH):
                fullAppUpdateObj = fullAppUpdateWorkflow.FullAppUpdate(workflowid)
            else:
                fullAppUpdateObj = installWorkflow.ProductInstall(workflowid)
            fullAppUpdateObj.workflowFullAppUpdatefalsetrue()
            
        if workflowid=="FullAppUpdatefalsefalseWorkflow":
            if StrictVersion(config.branch) >= StrictVersion(config.REVAMPED_APPS_PANEL_BRANCH):
                fullAppUpdateObj = fullAppUpdateWorkflow.FullAppUpdate(workflowid)
            else:
                fullAppUpdateObj = installWorkflow.ProductInstall(workflowid)
            fullAppUpdateObj.workflowFullAppUpdatefalsefalse()
            
        if workflowid=="FullAppUpdatetruetrueWorkflow":
            if StrictVersion(config.branch) >= StrictVersion(config.REVAMPED_APPS_PANEL_BRANCH):
                fullAppUpdateObj = fullAppUpdateWorkflow.FullAppUpdate(workflowid)
            else:
                fullAppUpdateObj = installWorkflow.ProductInstall(workflowid)
            fullAppUpdateObj.workflowFullAppUpdatetruetrue()
            
        if workflowid=="ThorUpdateWorkflow":
            selfUpdateObj=selfUpdate.selfUpdate(workflowid)
            selfUpdateObj.selfUpdateToLatestWorkflow()
        
        if workflowid=="ThorUpdateHopWorkflow":
            selfUpdateObj=selfUpdate.selfUpdate(workflowid)
            selfUpdateObj.selfUpdateHopWorkflow()
            
        if workflowid=="ThorUpdateSignoutSigninWorkflow":
            selfUpdateObj=selfUpdateSignoutSignin.selfUpdateSignoutSignin(workflowid)
            selfUpdateObj.selfUpdateToLatestSignoutSigninWorkflow()
            
        if workflowid=="ThorUpdateCCSignedinRunningWorkflow":
            selfUpdateObj=selfUpdateCCSignedinRunning.selfUpdateCCSignedinRunning(workflowid)
            selfUpdateObj.selfUpdateToLatestCCSignedinRunningWorkflow()
            
        if workflowid=="ThorUpdateCCNotRunningWorkflow":
            selfUpdateObj=selfUpdateCCNotRunning.selfUpdateCCNotRunning(workflowid)
            selfUpdateObj.selfUpdateToLatestCCNotRunningWorkflow()
            
        if workflowid=="ThorUpdateYetNewerVersionWorkflow":
            selfUpdateObj=selfUpdateYetNewerVersion.selfUpdateYetNewerVersion(workflowid)
            selfUpdateObj.selfUpdateYetNewerVersionWorkflow()
            
        if workflowid=="Sanity":
            sanityAppsObj=sanityAppsV2.SanityApps("Sanity-apps")
            sanityAppsObj.sanityAppsWorkflow()
            sanityLearnObj=sanityLearn.SanityLearn("Sanity-learn")
            sanityLearnObj.sanity_learn_workflow()
            sanityStocksObj=sanityStocks.sanityStocks("Sanity-stocks")
            sanityStocksObj.sanityStocksWorkflow()
            sanityBehanceObj=sanityBehance.sanityBehance("Sanity-behance")
            sanityBehanceObj.sanityBehanceWorkflow()
            sanityContainerObj=sanityContainer.sanityContainer("Sanity-container")
            sanityContainerObj.sanityContainerWorkflow()
        
        if workflowid=="Sanity-Assets":
            sanityFilesObj=sanityFiles.sanityFiles("Sanity-files")
            sanityFilesObj.sanityFilesWorkflow()
            sanityFontsObj=sanityFonts.sanityFonts("Sanity-fonts")
            sanityFontsObj.sanityFontsWorkflow()
            sanityMarketObj=sanityMarket("Sanity-market")
            sanityMarketObj.sanityMarketWorkflow()
            sanityAsyncObj=sanityAsync.SanityAsync("Sanity-async")
            sanityAsyncObj.sanityAsyncWorkflow()
            sanityUncObj = sanityUnc.SanityUnc("Sanity-unc")
            sanityUncObj.sanityUncWorkflow()
            
        if workflowid=="Sanity-container":
            sanityContainerObj=sanityContainer.sanityContainer("Sanity-container")
            sanityContainerObj.sanityContainerWorkflow()
        if workflowid=="Sanity-files":
            sanityFilesObj=sanityFiles.sanityFiles("Sanity-files")
            sanityFilesObj.sanityFilesWorkflow()
        if workflowid=="Sanity-fonts":
            sanityFontsObj=sanityFonts.sanityFonts("Sanity-fonts")
            sanityFontsObj.sanityFontsWorkflow()
        if workflowid=="Sanity-stocks":
            sanityStocksObj=sanityStocks.sanityStocks("Sanity-stocks")
            sanityStocksObj.sanityStocksWorkflow()
        if workflowid=="Sanity-behance":
            sanityBehanceObj=sanityBehance.sanityBehance("Sanity-behance")
            sanityBehanceObj.sanityBehanceWorkflow()
        if workflowid=="Sanity-market":
            sanityMarketObj=sanityMarket("Sanity-market")
            sanityMarketObj.sanityMarketWorkflow()
        if workflowid=="Sanity-apps":
            sanityAppsObj=sanityAppsV2.SanityApps("Sanity-apps")
            sanityAppsObj.sanityAppsWorkflow()
        if workflowid=="Sanity-learn":
            sanityLearnObj=sanityLearn.SanityLearn("Sanity-learn")
            sanityLearnObj.sanity_learn_workflow()
        if workflowid=="Sanity-async":
            sanityAsyncObj=sanityAsync.SanityAsync("Sanity-async")
            sanityAsyncObj.sanityAsyncWorkflow()
        if workflowid=="Sanity-unc":
            sanityUncObj = sanityUnc.SanityUnc("Sanity-unc")
            sanityUncObj.sanityUncWorkflow()
            
        if workflowid=="Acceptance-Market":
            marketAcceptanceObj=marketAcceptance.MarketAcceptanceCases("Acceptance-Market")
            marketAcceptanceObj.marketTestCases()
        if workflowid=="Acceptance-Files":
            filesAcceptanceObj=filesAcceptance.FileAcceptanceCases("Acceptance-Files")
            filesAcceptanceObj.filesTestCases()
        if workflowid=="Acceptance-Fonts":
            fontsAcceptanceObj= fontsAcceptance.FontsAcceptanceCases("Acceptance-Fonts")
            fontsAcceptanceObj.fontsTestCases()
        if workflowid == "Acceptance-Apps":
            appsAcceptanceObj = appsAcceptance.AppsAcceptanceCases("Acceptance-Apps")
            appsAcceptanceObj.appsTestCases()
        
        if workflowid=="UpdateAllWorkflow":
            updateAllWorkflowObj = updateAllWorkflow.UpdateAllWorkflow("UpdateAllWorkflow")
            updateAllWorkflowObj.updateAllWorkflow()
        
        if workflowid=='AppsLoadCFUPerformanceWorkflow':
            if iteration == None:
                iteration = 50
            resultId="CCAPPSLOAD"
            config.resultsObj=resultReporter.PerformanceResultDict(config.branch,config.buildno,config.environment,config.subscription)
            ccAppLoadPerformanceObj = ccAppsLoadPerformance.ccAppsLoadPerformance(workflowid)
            ccAppLoadPerformanceObj.CCAppsCheckForUpdates(iteration)
            
        if workflowid =='AppsLoadFreshLaunchPerformanceWorkflow':
            if iteration == None:
                iteration = 50
            resultId="CCAPPSLOAD"
            config.resultsObj=resultReporter.PerformanceResultDict(config.branch,config.buildno,config.environment,config.subscription)
            ccAppLoadPerformanceObj = ccAppsLoadPerformance.ccAppsLoadPerformance(workflowid)
            ccAppLoadPerformanceObj.ccAppsFreshLaunchPerformance(iteration)
            
        if workflowid =='AppsLoadResolveRefreshPerformanceWorkflow':
            if iteration == None:
                iteration = 50
            resultId="CCAPPSLOAD"
            config.resultsObj=resultReporter.PerformanceResultDict(config.branch,config.buildno,config.environment,config.subscription)
            ccAppLoadPerformanceObj = ccAppsLoadPerformance.ccAppsLoadPerformance(workflowid)
            ccAppLoadPerformanceObj.ccAppsResolveRefreshPerformance(iteration)
            
        if workflowid == "SingleAppInstallationWorkflow":
            resultId = "SINGLE_APP_INSTALL"
            singleAppInstallWorkflowObj = singleAppInstallWorkflow.SingleAppInstall(workflowid)
            singleAppInstallWorkflowObj.singleAppInstallWorkflow()
            
        if workflowid=="AppsRCWorkflow":
            appsRCWorkflowObj=appsRCWorkflow.appsRCWorkflow(workflowid)
            appsRCWorkflowObj.apps_RC_workflow()
            
        if workflowid=="AppsRCWorkflow2":
            appsRCWorkflowObj = appsRCWorkflow2.AppsRCWorkflow2(workflowid)
            appsRCWorkflowObj.appsRCWorkflow2()
            
        if workflowid=="AppsAutoUpdateWorkflow":
            appsAutoUpdateWorkflowObj=appsAutoUpdateWorkflow.appsAutoUpdateWorkflow(workflowid)
            appsAutoUpdateWorkflowObj.apps_Auto_Update_workflow()
            
            
        if workflowid=="ASURCWorkflow":
            ASURCWorkflowObj=ASURCWorkflow.ASURCWorkflow(workflowid)
            ASURCWorkflowObj.ASU_RC_workflow()
        
        if workflowid == "DirtyMachineWorkflow":
            resultId = "SINGLE_APP_INSTALL"
            
            dirtyMachineWorkflowObj = dirtyMachineWorkflow.DirtyMachineWorkflow(workflowid)
            dirtyMachineWorkflowObj.dirtyMachineWorkflowRunner()

        if workflowid == "ProductInstallUninstallWorkflow":
            workflowObj = productInstallUninstallWorkflow.ProductInstallUninstallWorkflow(workflowid)
            workflowObj.productInstallUninstallScenarios()
            
        if workflowid=="HDEngineRCWorkflow":
            HDEngineRCWorkflowObj = HDEngineRCWorkflow.HDEngineRCWorkflow("HDEngineRCWorkflow")
            HDEngineRCWorkflowObj.HDEngineRCWorkflow()
             
            
    except Exception,e:
        config.logObj.critical('Error: Catching exception in workflow runner - ' + str(e))
        config.screenShotObj.captureScreen()
        workflowRunnerExecutionStatus=False
    
    try:
     
        #Display list of running processes and raise alert if Explorer.exe is in system mode
        basicThorUtils.alertExplorerSystemMode()
     
         
        #Upload coverage file for Instrumented build
        if config.LBS_LOCATION.lower() == 'instrumented':
            config.logObj.info("Uploading Coverage file for instrumented build.")
            if os.name == 'nt':
                covfile_path = os.path.join('C:/', 'test.cov')
               
            #Uploading to FTP
            serverFileUrl = "/THOR_BUILDS/Instrumented/WIN/" + str(config.branch) + "/" + str(config.buildno) + '/Coverage_Files/' + config.screenShotObj.getTimeStamp() + '_test.cov'
            ftputils.uploadFileToFTPServer(config.thorftpserver, covfile_path, serverFileUrl, config.LOGFTPUSERNAME, config.LOGFTPPASSWORD)
            config.logObj.info("Uploaded Coverage file.")
           
        ftpServerFilePath=config.screenShotObj.uploadScreenShots()
        config.resultsObj.updateResultScreenshotZipPath(ftpServerFilePath)
        try:
            if mode=="run":
                config.dashboardDb.dumpData(config.resultsObj.getResultJson(), "Completed")
            print config.resultsObj.getResultJson()
        except Exception,e:
            config.logObj.critical('Error: Catching exception in dumpDdata ' + str(e))            
        htmlGenerator.HtmlReporter().generateSimpleHTML(config.resultsObj.getResultDictInStr(),resultId)
         
        ''' Send report via thorqe@adobe.com'''
        if workflowid in ["UpdateAllWorkflow", "SingleAppInstallationWorkflow"] and mode == "run":
            MAIL_LIST=config.MAIL_LIST_MANAGERS
            OS_NAME= machineInfo.machineName()
            resultFilePath = os.path.join(os.path.dirname(__file__),"thor","resultreporter","result.html")
            if os.path.exists(resultFilePath):
                with open(resultFilePath,'r') as f:
                    mailUtils.sendMail(MAIL_LIST, workflowid+" | ACC "+config.branch+" | Build# "+config.buildno+" | "+OS_NAME+" | Environment: "+config.environment+" | ID: "+config.subscription, f.read(), config.MAIL_ID_THORQE)
            
        if config.threadDataStream != "" and mode == "run" and workflowid == "UpdateAllWorkflow":
            MAIL_LIST=config.MAIL_LIST_AUTO
            OS_NAME= machineInfo.machineName()
            mailUtils.sendMail(MAIL_LIST, "CEF MEMORY USAGE | "+workflowid+" | ACC "+config.branch+" | Build# "+config.buildno+" | "+OS_NAME+" | Environment: "+config.environment+" | ID: "+config.subscription, config.threadDataStream, config.MAIL_ID_THORQE)
           
        config.seleniumObj.close()
        basicThorUtils.quitCreativeCloud()
         
    except Exception,e:
        config.logObj.critical('Error: Catching exception in workflow runner while uploading and updating data ' + str(e))
        workflowRunnerExecutionStatus=False
#Disable RDCM call as our new Openstack RDUtility is workflow independant
#     if mode == "run":
#         rdcObj.updateDB('0')
    if config.adobeid:
        accountService.freeId(config.adobeid)
    config.logObj.info('Collecting logs at the end of workflow')
    basicThorUtils.uploadLogsToServer()
    logger.uploadLogFile(workflowid,branch,buildno)
     
    if not workflowRunnerExecutionStatus:
        sys.exit(1)

'''
Created on Jul 13, 2015
@author: sarthak
'''
import os
import thor.commonutils.basicutils as basicThorUtils

environment=None
usePassedEnvironment=None
branch=None
buildno=None
resultsObj=None
screenShotObj=None
subscription=None
adobeid=None
adobeidPass=None
idtype=None
logObj = None
ffcStack=None
threadDataStream = ""
dashboardDb = None
locale = None
string = None
workflowid = None
ASUBranch = None
ASUBuildno = None
seleniumObj=None
mode=None
CCApps = None


#Use NonElevatedACC launched by stduser
useNonElevatedACC = False

webUIWebDriversObj={}
SignInHandle="Sign"
HostHandle="host"
CreativeCloudHandle="Cloud"
TermsOfUseScreenHandle="Complete"
PhoneScreenHandle="phone"
BundleIDCC="com.adobe.acc.AdobeCreativeCloud"
accountPoolService="http://thorlogs.corp.adobe.com:3333"
thorftpserver="thorlogs.corp.adobe.com"
thorftpserver2="thorlogs2.corp.adobe.com"
thorhttpserver="http://thorlogs.corp.adobe.com"
thorhttpserver2="http://thorlogs2.corp.adobe.com"
LOGFTPPASSWORD="thor"
LOGFTPUSERNAME="thor"
BASELOGSPATH="/thor/logs/"
BASESCREENSHOTSPATH="/thor/screenshots/"
# CREATIVECLOUDFILESURLPROD="https://assets2.adobe.com/files"
# CREATIVECLOUDFILESURLSTAGE="https://assets2-stage.adobecc.com/files"
CREATIVECLOUDFILESURLPROD="https://assets2.adobe.com/"
CREATIVECLOUDFILESURLSTAGE="https://assets2-stage.adobecc.com/"
CREATIVECLOUDFILESURLNEWPROD="https://assets.adobe.com/files"
CREATIVECLOUDFILESURLNEWSTAGE="https://assets-stage.adobecc.com/files"
PRIVATECLOUDURLPROD="https://ccems-prod-9-org1-useast1.adobecce.com"
PRIVATECLOUDURLSTAGE="https://ccems-stage-1-org1-uswest1.adobemsccep.com"
FONTSURLPROD="https://typekit.com"
FONTSURLSTAGE="https://relstage.typekit.com"
CCMDLSADOBEURL="https://ccmdls.adobe.com"
uandrAccountPoolService="http://thorlogs.corp.adobe.com:3335"
BEHANCESTAGEURL="https://net.s2stagehance.com/"
BEHANCEPRODURL="https://www.behance.net/"
FTP_LOG_FILE_PATH = "/thor/automationLogs/"
FFC_PROD_URL1='prod-rel-ffc-ccm.oobesaas.adobe.com'
FFC_PROD_URL2='prod-rel-ffc.oobesaas.adobe.com'
FFC_GREEN_STACK_URL='green-ffc.oobesaas.adobe.com'
FFC_BLUE_STACK_URL='blue-ffc.oobesaas.adobe.com'
REVAMPED_APPS_PANEL_BRANCH = '4.2.5'
A_DOT_COM_STAGE_URL = "https://www.stage.adobe.com/"
A_DOT_COM_PROD_URL = "https://www.adobe.com"
A_DOT_COM_PRODUCT_CATALOG_URL_PROD = "https://www.adobe.com/creativecloud/catalog/desktop.html"
A_DOT_COM_PRODUCT_CATALOG_URL_STAGE = "https://www.stage.adobe.com/creativecloud/catalog/desktop.html"
NGL_TRIAL_RESET_URL_STAGE = "https://lcs-entitlement-stage.adobe.io/v1/ngltrials"
NGL_TRIAL_RESET_URL_PROD = "https://lcs-entitlement.adobe.io/v1/ngltrials"
EXIT_ON_FAILURE = True
ADOBE_ACCOUNT_PAGE_URL= "account.adobe.com"
ADOBE_ACCOUNT_PROFILE_PAGE_URL= "account.adobe.com/profile"
if os.name=="nt":

    UserProfilePath = os.getenv("USERPROFILE") 
    AutomationStartedCheckFilePath="C:\AutomationStarted.txt"
    ThorBaseLocation="C:\\Thor"
    AAM_UPDATER_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Adobe", "AAMUpdater","1.0")
    DLM_LOG_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Temp", "CreativeCloud","ACC","AdobeDownload")
    DLM_LOG_FILE_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Temp", "CreativeCloud","ACC","AdobeDownload","DLM.log")
    ThorAppReferencePath=r"Adobe\Adobe Creative Cloud\ACC\Creative Cloud.exe"
    ThorAppPath = os.path.join(basicThorUtils.get_ProgramFiles_Path(), ThorAppReferencePath)
    ThorProcessListAll=['Creative Cloud', 'CEPServiceManager', 'CoreSync', 'unsecapp','Adobe CEF Helper','AdobeIPCBroker','Adobe Desktop Service','CCLibrary']
    ThorProcessListElevationCheck=['Creative Cloud', 'CoreSync','Adobe CEF Helper','AdobeIPCBroker','Adobe Desktop Service','CCLibrary','CCXProcess']
    ThorProcessListLaunch=['Creative Cloud','CoreSync','Adobe CEF Helper','AdobeIPCBroker','Adobe Desktop Service']
    SoftQuitThorProcessList = ['Creative Cloud']
    RedirectionServerPath=thorhttpserver+"/redirection/Redirection.exe"
    LocalRedirectionPath=os.path.join(ThorBaseLocation,"Redirection.exe")
    OOBETempDirectory=os.path.join(UserProfilePath,"AppData","Local","Adobe","OOBE")
    PII_PATH = os.path.join(UserProfilePath,"AppData", "Local", "Adobe","PII","com.adobe.pii.prefs")
    FFCXMLPATH="\\ProgramData\\Adobe\\OOBE\\ffc"
    DESKTOPPATH=os.path.join(UserProfilePath,"Desktop")
    LogCollectorServerPath=thorhttpserver+"/logcollector/LogCollectorTool.exe"
    LocalLogCollectorPath=os.path.join(ThorBaseLocation,"LogCollectorTool.exe")
    LogCollectorServerPath_New = thorhttpserver+"/logcollector/New/LogCollectorToolWin.zip"
    LocalLogCollectorPathZipped_New = os.path.join(ThorBaseLocation,"LogCollectorToolWin.zip")
    LocalThorBuildServer="http://thor-lbs-win1.corp.adobe.com/AdobeProducts/win32"
    ThorUninstallerPath = os.path.join(basicThorUtils.get_ProgramFiles_Path(),'Adobe', 'Adobe Creative Cloud', 'Utils', 'Creative Cloud Uninstaller.exe')
    ThorUninstallerName="Creative Cloud Uninstaller.exe"
    ThorInstallationFolderPath=os.path.join(basicThorUtils.get_ProgramFiles_Path(),'Adobe', 'Adobe Creative Cloud')
    AdobeLocalFolderPath=os.path.join(os.getenv('LOCALAPPDATA'), 'Adobe')
    AdobeRoamingFolderPath=os.path.join(os.getenv('APPDATA'), 'Adobe')
    AdobeCommonOOBEFolderPath=os.path.join(basicThorUtils.get_ProgramFiles_Path(), 'Common Files','Adobe','OOBE')
    ASUInstalledPath=os.path.join(AdobeCommonOOBEFolderPath,"PDApp")
    serviceConfigXMLPath=os.path.join(AdobeCommonOOBEFolderPath,"configs")
    AdobeDesktopCommonFolderPath=os.path.join(basicThorUtils.get_ProgramFiles_Path(), 'Common Files','Adobe','Adobe Desktop Common')
    ThorCreativeCloudFilesFolder=os.path.join(UserProfilePath, 'Creative Cloud Files')
    CREATIVECLOUDSETUPEXE="CreativeCloudSet-Up.exe"
    INSTALLER_LOG_PATH = os.path.join(basicThorUtils.get_ProgramFiles_Path(),'Common Files','Adobe','Installers')
    HD_LOG_PATH = os.path.join(INSTALLER_LOG_PATH,'Install.log')
    ThorProdApplicationsXmlUrl="https://prod-rel-ffc.oobesaas.adobe.com/adobe-ffc-external/core/v1/applications?name=CreativeCloud&name=CCLBS&osVersion=6.1.1&platform=win32&version="
    ACC_LOG_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Temp",'CreativeCloud','ACC',"ACC.log")
    PDAPP_LOG_PATH = os.path.join(UserProfilePath, "AppData", "Local", "Temp","CreativeCloud","ACC.log")
    HOSTS_FILE_PATH="\\Windows\\System32\\drivers\\etc\\hosts"
    CRASH_DUMPS_PATH= os.path.join(os.getenv('LOCALAPPDATA'), 'CrashDumps')
    CHROME_DRIVER_PATH = os.path.join(os.path.dirname(__file__), 'thor', 'uiutils', 'chromedriver.exe') 
    CEF_FILE_PATH = os.path.join(basicThorUtils.get_ProgramFiles_Path(),"Common Files","Adobe","Adobe Desktop Common","HEX","cef.debug")
    HDPIM_FILE_PATH = os.path.join(basicThorUtils.get_ProgramFiles_Path(),"Common Files","Adobe","caps","hdpim.db")
    COSY_INSTALLATION_PATH = os.path.join(basicThorUtils.get_ProgramFiles_Path(),'Adobe', 'Adobe Sync')
    KaizenDebugFilePath = r"\resources\HTMLViewTester.dll"
    KaizenDllPath = os.path.join(os.getenv("CommonProgramFiles"), "Adobe")
    NEW_CCLIBRARIES_PATH = os.path.join(basicThorUtils.get_ProgramFiles_Path(),"Common Files","Adobe","Creative Cloud Libraries")
    UNC_VERSION_FILE_Path = os.path.join(basicThorUtils.get_ProgramFiles_Path(), "Adobe", "Adobe Creative Cloud", "ACC", "resource", "ui", "unc", "version.json")
    LRCC_FOLDER_PATH=r"C:\Program Files\Adobe\Adobe Lightroom Classic CC"
    UNINSTALL_XML_PATH=os.path.join(INSTALLER_LOG_PATH,'uninstallXml')
    ProductApplicationsJsonUrl="https://cdn-ffc.oobesaas.adobe.com/core/v2/applications?platform=win64"
    PDB_DB_PATH=os.path.join(basicThorUtils.get_ProgramFiles_Path(),"Common Files","Adobe","caps")
else:
    UNC_VERSION_FILE_Path="/Applications/Utilities/Adobe Creative Cloud/ACC/resource/ui/unc/version.json"
    AutomationStartedCheckFilePath="/AutomationStarted.txt"
    ThorBaseLocation="/Volumes/Safe/Thor"
    ThorAppPath="/Applications/Utilities/Adobe Creative Cloud/ACC/Creative Cloud.app"
    ASUInstalledPath="/Applications/Utilities/Adobe Application Manager/"
    ThorProcessListAll=['Creative Cloud', 'Adobe Desktop Service', 'Core Sync','CCLibrary','CCXProcess','node','Adobe CEF Helper','AdobeCrashDaemon', 'AdobeCRDaemon','CEPServiceManager','AdobeIPCBroker']
    ThorProcessListLaunch=['Creative Cloud', 'Core Sync','Adobe CEF Helper','AdobeIPCBroker','Adobe Desktop Service','node']
    SoftQuitThorProcessList = ['Creative Cloud']
    UserVolume = os.getenv("HOME")
    UserProfilePath=UserVolume
    DLM_LOG_PATH = os.path.join(UserVolume, "Library", "Logs","CreativeCloud","ACC", "AdobeDownload")
    DLM_LOG_FILE_PATH = os.path.join(UserVolume, "Library", "Logs","CreativeCloud","ACC","AdobeDownload","DLM.log")
    ACC_LOG_PATH = os.path.join(UserVolume, "Library","Logs",'CreativeCloud','ACC',"ACC.log")
    PDAPP_LOG_PATH = os.path.join(UserVolume, "Library","Logs","CreativeCloud","ACC.log")
    OOBEFolderPath = os.path.join(UserVolume,"Library", "Application Support", "Adobe","OOBE")
    generalPreferenceFilePath = os.path.join(OOBEFolderPath, "com.adobe.acc.default.prefs")
    RedirectionServerPath=thorhttpserver+"/redirection/Redirection.zip"
    LocalRedirectionPathZipped=os.path.join(ThorBaseLocation,"Redirection.zip")
    LocalRedirectionPath=os.path.join(ThorBaseLocation,"Redirection")
    PII_PATH = os.path.join(UserVolume,"Library", "Application Support", "Adobe","PII","com.adobe.pii.prefs")
    FFCXMLPATH="/Users/Shared/Adobe/OOBE/ffc"
    OOBETempDirectory=OOBEFolderPath
    DESKTOPPATH=os.path.join(UserVolume,"Desktop")
    LogCollectorServerPath=thorhttpserver+"/logcollector/LogCollectorTool.zip"
    LocalLogCollectorPathZipped=os.path.join(ThorBaseLocation,"LogCollectorTool.zip")
    LocalLogCollectorPath=os.path.join(ThorBaseLocation,"LogCollectorTool.app/Contents/MacOS/LogCollectorUI")
    LogCollectorServerPath_New = thorhttpserver+"/logcollector/New/LogCollectorToolMac.zip"
    LocalLogCollectorPathZipped_New = os.path.join(ThorBaseLocation,"LogCollectorToolMac.zip")
    LocalThorBuildServer="http://thor-lbs-mac2.corp.adobe.com/AdobeProducts/osx10"
    ThorInstallationFolderPath="/Applications/Utilities/Adobe Creative Cloud"
    CREATIVECLOUDSETUPEXE="Creative Cloud Installer"
    INSTALLER_LOG_PATH=r'/Library/Logs/Adobe/Installers'
    HD_LOG_PATH = os.path.join(INSTALLER_LOG_PATH,'Install.log')
    ThorProdApplicationsXmlUrl="https://prod-rel-ffc.oobesaas.adobe.com/adobe-ffc-external/core/v1/applications?name=CreativeCloud&name=CCLBS&osVersion=10.12.0&platform=osx10&version="
    ThorCreativeCloudFilesFolder=os.path.join(os.getenv('HOME'), 'Creative Cloud Files')
    HOSTS_FILE_PATH=r"/private/etc/hosts"
    CRASH_DUMPS_PATH= os.path.join(UserVolume, "Library", "Logs", "DiagnosticReports")
    CHROME_DRIVER_PATH = os.path.join(os.path.dirname(__file__), 'thor', 'uiutils', 'chromedriver') 
    CEF_FILE_PATH = r'/Library/Application Support/Adobe/Adobe Desktop Common/HEX/cef.debug'
    serviceConfigXMLPath = r'/Library/Application Support/Adobe/OOBE/configs/'
    HDPIM_FILE_PATH = r'/Library/Application Support/Adobe/caps/hdpim.db'
    COSY_INSTALLATION_PATH = "/Applications/Utilities/Adobe Sync"
    AdobeDesktopCommonFolderPath = '/Library/Application Support/Adobe/Adobe Desktop Common'
    KaizenDebugFilePath =  r"/resources/HTMLViewTester.dylib"
    KaizenDllPath=r'/Library/Application Support/Adobe'
    NEW_CCLIBRARIES_PATH = '/Library/Application Support/Adobe/Creative Cloud Libraries'
    UNINSTALL_XML_PATH='/Library/Application Support/Adobe/Installers/uninstallXml'
    LRCC_FOLDER_PATH='/Applications/Adobe Lightroom Classic CC'
    HDBOX_FOLDER_LOC=os.path.join(UserVolume,"Library", "Application Support", "Adobe","Adobe Desktop Common","HDBox")
    UNINSTALL_ALIAS_PATH=r"/Applications/Utilities/Adobe Installers/"
    ProductApplicationsJsonUrl="https://cdn-ffc.oobesaas.adobe.com/core/v2/applications?platform=osx10"
    PDB_DB_PATH=os.path.join(UserVolume,"Library", "Application Support", "Adobe","caps")

MARKET_ASSETS_DOWNLOAD_LOCATION = os.path.join(ThorCreativeCloudFilesFolder, "Market Downloads")
DEFAULT_LIBRARY_NAME = "My Library"
hdProductList=["Illustrator CC (2015)","Experience Design CC (Preview)"]
LOCALHTTPFOLDERPATH=os.path.join(ThorBaseLocation,"HTTP")
APPLICATIONXMLNAME="applications.xml"
APPLICATIONJSONNAME="applications.json"
FESXMLNAME="fes.xml"
APPLICATIONXMLPATH=os.path.join(LOCALHTTPFOLDERPATH,APPLICATIONXMLNAME)
APPLICATIONJSONPATH=os.path.join(LOCALHTTPFOLDERPATH,APPLICATIONJSONNAME)
FESXMLPATH=os.path.join(LOCALHTTPFOLDERPATH,FESXMLNAME)
PIMDBFILEPATH=os.path.join(ThorInstallationFolderPath,"pim.db")

''' Mail list'''
MAIL_LIST_AUTO = ['shansari@adobe.com', 'rewari@adobe.com']
MAIL_LIST_LEAD = ['shansari@adobe.com', 'rewari@adobe.com', 'vitalwar@adobe.com', 'rohitkum@adobe.com', 'vvarshne@adobe.com', 'bhatnaga@adobe.com', 'gaul@adobe.com']
MAIL_LIST_MANAGERS = ['shansari@adobe.com', 'rewari@adobe.com', 'vitalwar@adobe.com', 'bhatnaga@adobe.com']
MAIL_ID_THORQE = 'thorqe@adobe.com'

'''Codex Build Download information'''
CODEXPRODUCTNAME = "ACCC"
CODEXSUBPRODUCT = "Application"
if os.name=="nt":
    CODEXPLATFORM = "win32"
    ASUINSTALLERNAME = "ApplicationManager10.0_all.exe"
else:
    CODEXPLATFORM = "osx10"
    ASUINSTALLERNAME = "ApplicationManager10.0_all.dmg"

CODEXLANGUAGE = "mul"
CODEXLICENSEMODEL = "Retail"
CODEXFORMATNAME = "ESD"
CODEXSTATUSNAME = "Available"
GENERICUSERNAME = "thorqe"
GENERICPASSWORD = "AdobeIndia#21"
CODEXCOMPLILETARGET= "Release"

'''Codex Build Download information'''
ASUCODEXPRODUCTNAME = "Adobe Setup Utility"
ASUCODEXSUBPRODUCT = "Library"
ASUCODEXFORMATNAME = "Folder"
ASUCODEXLICENSEMODEL = "Volume"

BEHANCE_PROJECT = {
        "utagarwa+trial10@adobetest.com": "47296929/Automation-test-project",
        "utagarwa+automation_trial_id@adobetest.com": "47297033/Automation-test-project",
        "utagarwa+stage_paid_id@adobetest.com": "1208507/Automation-test-project",
        "utagarwa+automation+trial+stg@adobetest.com": "1208505/Automation-test-project",
        "rohitkum+automation_p1@adobetest.com": "47345579/Automation-test-project",
        "rohitkum+automation_p2@adobetest.com": "47345705/Automation-test-project",
        "rohitkum+automation_p3@adobetest.com": "47345805/Automation-test-project",
        "rohitkum+autotrial_p1@adobetest.com": "47345857/Automation-test-project",
        "rohitkum+autotrial_p2@adobetest.com": "47346003/Automation-test-project",
        "savarshn+autotrial_p1@adobetest.com": "47346071/Automation-test-project",
        "rohitkum+autotrial_s1@adobetest.com": "1208809/Automation-test-project",
        "rohitkum+autotrial_s2@adobetest.com": "1208811/Automation-test-project",
        "rohitkum+autotrial_s3@adobetest.com": "1208813/Automation-test-project",
        "rohitkum+automation_s1@adobetest.com": "1208815/Automation-test-project",
        "rohitkum+automation_s2@adobetest.com": "1208819/Automation-test-project",
        "rohitkum+automation_s3@adobetest.com": "1208821/Automation-test-project",
        "rohitkum+automation_s3@adobetest.com": "1208823/Automation-test-project",
        "shansari+automation48@adobetest.com":"65287827/Automation-test-project",
        "shansari+automation49@adobetest.com":"65287651/Automation-test-project",
        "shansari+automation50@adobetest.com":"65287567/Automation-test-project",
        "shansari+automation51@adobetest.com":"65287317/Automation-test-project",
        "shansari+automation52@adobetest.com":"65286883/Automation-test-project"
}


BEHANCE_USER_ID = {
        "utagarwa+trial10@adobetest.com": "utagarwatr8e5a",
#         "utagarwa+automation_trial_id@adobetest.com": "47297033/Automation-test-project",
        "utagarwa+stage_paid_id@adobetest.com": "utagarwast30ba",
#         "utagarwa+automation+trial+stg@adobetest.com": "1208505/Automation-test-project",
        "rohitkum+automation_p1@adobetest.com": "rohitkumau24e3",
        "rohitkum+automation_p2@adobetest.com": "rohitkumauee42",
        "rohitkum+automation_p3@adobetest.com": "rohitkumaubae4",
#         "rohitkum+autotrial_p1@adobetest.com": "47345857/Automation-test-project",
#         "rohitkum+autotrial_p2@adobetest.com": "47346003/Automation-test-project",
#         "savarshn+autotrial_p1@adobetest.com": "47346071/Automation-test-project",
#         "rohitkum+autotrial_s1@adobetest.com": "1208809/Automation-test-project",
#         "rohitkum+autotrial_s2@adobetest.com": "1208811/Automation-test-project",
#         "rohitkum+autotrial_s3@adobetest.com": "1208813/Automation-test-project",
        "rohitkum+automation_s1@adobetest.com": "rohitkumau0d7a",
        "rohitkum+automation_s2@adobetest.com": "rohitkumaucdc5",
        "rohitkum+automation_s3@adobetest.com": "rohitkumau765e",
        "shansari+automation48@adobetest.com":"shansariaucdb7",
        "shansari+automation49@adobetest.com":"shansariau3ac2",
        "shansari+automation50@adobetest.com":"shansariau3a22",
        "shansari+automation51@adobetest.com":"shansariau3e19",
        "shansari+automation52@adobetest.com":"shansariaub6ab"
}


NOT_COMPATIBLE_PRODUCTS = {
    'SPRK': ["Windows 7 32bit", "Windows 7 64bit", "Windows 8 32bit", "Windows 8 64bit"]
}

RUN_CURL_SCRIPT = False
LBS_LOCATION = "localserver"
CHROME_PROFILE = None
ADOTCOM_PRODUCT_DOWNLOAD_URL_PROD = "http://creative.adobe.com/products/download/" #Append product name i.e- creative-cloud
ADOTCOM_PRODUCT_DOWNLOAD_URL_STAGE = "https://stage.ccmui.adobe.com/products/download/" #Append product name i.e- creative-cloud

#Flag for updating fes.xml file
UPDATE_FES = None
#If using older LBS instead of Kaizen installer of thor
USE_LEGACY_LBS = False


#System utilization object
sys_util_obj = None

#Variable to control no of iterations
iteration = None

'''
    Bluestreak XMLs - BSE, BSD, HTTP
'''
BSE_ENABLED = '''    
    <feature-entry id="com.adobe.oobe.acc.v1.useBluestreakExtraction" state="ENABLED">
        <data>ALL</data>
    </feature-entry>  
'''
BSE_DISABLED = '''
    <feature-entry id="com.adobe.oobe.acc.v1.useBluestreakExtraction" state="DISABLED">
        <data>ALL</data>
    </feature-entry>  
'''
BSD_ENABLED = '''
    <feature-entry id="com.adobe.oobe.acc.v1.useBluestreakDownload" state="ENABLED">
        <data>ALL</data>
    </feature-entry>
'''
BSD_DISABLED = '''
    <feature-entry id="com.adobe.oobe.acc.v1.useBluestreakDownload" state="DISABLED">
        <data>ALL</data>
    </feature-entry>
'''
HTTP_ENABLED = '''
    <feature-entry id="com.adobe.oobe.acc.v1.useSecureUrlForBitsDownload" state="ENABLED"/>
'''
HTTP_DISABLED = '''
    <feature-entry id="com.adobe.oobe.acc.v1.useSecureUrlForBitsDownload" state="DISABLED"/>
'''


TYPEKIT_REBRANDING = {'prod': False, 'stage': True}


'''
    IMPORTANT: DO NOT USE ADDITIONAL ARGUMENTS. USE extras 
'''
extras = {}

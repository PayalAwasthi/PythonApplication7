'''
This file is for testing purposes only.
Created on Jul 21, 2015

@author: sarthak
'''
import argparse, sys, os, time
import config
import thor.commonutils.accountpoolservice as accountService
import thor.commonutils.basicutils as basicThorUtils
import thor.commonutils.installerutils as installUtils
import thor.commonutils.loggerUtils as loggerUtils
import thor.commonutils.screencapture as screenCapture
import thor.commonutils.stringsHandler as stringsHandler
import thor.resultreporter.resultdict as resultReporter
import thor.uiutils.seleniumutils as utils
import thor.panels.apps.AppsPanelv2 as appsPanel
import thor.panels.assets.assetspanel as assetsPanel
import thor.panels.community.communitypanel as communityPanel
import thor.panels.container.containerpanel as containerPanel
import thor.panels.home.homepanel as homePanel
import thor.panels.stocks.stockspanel as stocksPanel
import workflow.sanity.sanityapps as sanityApps
import thor.commonutils.ffcxmlutils as ffcxmlutils
import thor.commonutils.fesxmlutils as fesxmlutils
import thor.commonutils.basicutils as basicutils
import workflow.sanity.sanity_learn as sanity_learn
import thor.panels.learn.learn_panel as learn_panel
from datetime import datetime

if __name__ == '__main__':
    
    config.environment="prod"
    config.branch="4.4"
    config.buildno="192.s"
    config.adobeid="paawasth@adobe.com"
    config.adobeidPass="Bap@d0be"
    config.subscription="paid"
    workflowid="selfupdateworkflow"
    config.string = stringsHandler.getData(config.locale)
    logger = loggerUtils.Logger()
    
#     installUtils.installThorUsingLBS(config.branch, config.buildno)
    basicThorUtils.launchCreativeCloud()

    config.resultsObj=resultReporter.ResultDict(config.branch,config.buildno,config.environment,config.subscription)
    config.screenShotObj=screenCapture.ScreenCapture()
    config.seleniumObj=utils.SeleniumUtils()
    
    appsPanelObj = appsPanel.AppsPanel("HTML")
    assetsPanelObj = assetsPanel.AssetsPanel("HTML")
    communityPanelObj = communityPanel.CommunityPanel("HTML")
    containerPanelObj = containerPanel.ContainerPanel("HTML")
    homePanelObj = homePanel.homePanel("HTML")
    stocksPanelObj = stocksPanel.StocksPanel("HTML")

    containerPanelObj.waitGlobalSpinner()
    containerPanelObj.signInACC(config.adobeid, config.adobeidPass, config.idtype)
    containerPanelObj.waitGlobalSpinner()
    if containerPanelObj.isHomeTabVisible():
        config.logObj.info("Sign In passed, Home tab visible")
    else:
        config.logObj.critical("Sign in failed")
    

     
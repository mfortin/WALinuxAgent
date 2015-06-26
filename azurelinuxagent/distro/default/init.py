# Windows Azure Linux Agent
#
# Copyright 2014 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires Python 2.4+ and Openssl 1.0+
#

import os
import azurelinuxagent.conf as conf
import azurelinuxagent.logger as logger
from azurelinuxagent.utils.osutil import OSUtil
import azurelinuxagent.utils.fileutil as fileutil


class InitHandler(object):
    def init(self, verbose):
        #Init stdout log
        level = logger.LogLevel.VERBOSE if verbose else logger.LogLevel.INFO
        logger.AddLoggerAppender(logger.AppenderType.STDOUT, level)

        #Init config
        configPath = OSUtil.GetConfigurationPath()
        conf.LoadConfiguration(configPath)
        
        #Init log
        verbose = verbose or conf.GetSwitch("Logs.Verbose", False)
        level = logger.LogLevel.VERBOSE if verbose else logger.LogLevel.INFO
        logger.AddLoggerAppender(logger.AppenderType.FILE, level,
                                 path="/var/log/waagent.log")
        logger.AddLoggerAppender(logger.AppenderType.CONSOLE, level,
                                 path="/dev/console")
        
        #Create lib dir
        fileutil.CreateDir(OSUtil.GetLibDir(), mode=0700)
        os.chdir(OSUtil.GetLibDir())



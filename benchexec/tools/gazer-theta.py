# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.result as result
import benchexec.tools.template


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for gazer-theta
    (combined tool of Gazer and Theta)
    https://github.com/ftsrg/gazer
    https://github.com/ftsrg/theta
    """

    REQUIRED_PATHS = ["gazer", "gazer/tools/gazer-bmc", "gazer/tools/gazer-theta"]

    def executable(self, tool_locator):
        return tool_locator.find_executable("gazer_starter.py", subdir="gazer/scripts")

    def name(self):
        return "gazer-theta"

    def version(self, executable):
        return self._version_from_tool(executable)

    def cmdline(self, executable, options, task, rlimits):
        assert len(list(task.input_files_or_identifier)) == 1
        # possible option: --output (default value if flag isn't used: working directory)
        return [executable] + options + list(task.input_files_or_identifier)

    def determine_result(self, run):
        status = result.RESULT_UNKNOWN
        if run.was_timeout:
            status = "TIMEOUT"
        else:
            for line in run.output:
                if "Result of gazer-theta run: FALSE" in line:
                    status = result.RESULT_FALSE_REACH
                elif "Result of gazer-theta run: TRUE" in line:
                    status = result.RESULT_TRUE_PROP

        if status == result.RESULT_UNKNOWN and run.exit_code.value != 0:
            status = result.RESULT_ERROR

        return status

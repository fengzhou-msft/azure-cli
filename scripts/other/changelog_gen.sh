#!/usr/bin/env bash                                                                                                                                                                                                         
set -exv 
module=$1
echo $module

cd /azure-sdk-for-python
python -m packaging_tools.code_report --last-pypi azure-mgmt-$module 2> tmp_last.output
python -m packaging_tools.code_report azure-mgmt-$module 2> tmp_current.output

report_last=$(grep "Merged report written to" tmp_last.output |sed -e 's/\(.*\)Merged report written to \(.*\)/\2/')
if [ -z "$report_last" ]
then
    report_last=$(grep "Report written to" tmp_last.output |sed -e 's/\(.*\)Report written to \(.*\)/\2/')
fi

report_current=$(grep "Merged report written to" tmp_current.output |sed -e 's/\(.*\)Merged report written to \(.*\)/\2/')
if [ -z "$report_current" ]
then    
    report_current=$(grep "Report written to" tmp_current.output |sed -e 's/\(.*\)Report written to \(.*\)/\2/')
fi
rm tmp_last.output tmp_current.output

python -m packaging_tools.change_log $report_last $report_current



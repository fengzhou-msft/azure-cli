#!/usr/bin/env bash                                                                                                                                                                                                         
set -exv 
branch=$1
module=$2
echo $branch

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -b|--branch)
    branch="$2"
    shift # past argument
    shift # past value
    ;;
    -m|--module)
    module="$2"
    shift # past argument
    shift # past value
    ;;
    -n|--newbranch)
    newbranch="$2"
    shift # past argument
    ;;
    *)    # unknown option
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters


cd /azure-rest-api-specs
git checkout master                                                                                                                                                                                                      
git pull         

cd ../azure-sdk-for-python                                                                                                                                                                                           
if $newbranch; then
  git checkout master
  git pull
  git checkout -b $branch
else
  git fetch 
  git checkout -b $branch origin/$branch                    
fi

python -m packaging_tools.generate_sdk -v -m ../azure-rest-api-specs/specification/$module/resource-manager/readme.md
git status

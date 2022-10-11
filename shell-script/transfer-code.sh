#!/bin/bash

read -p "Input your prj group name: " group
echo "your prj group name is: ${group}"
read -p "Input your prj name: " prj_name
echo "your prj name is: ${prj_name}"

dir_prj=`ls  | grep -w ^${prj_name}$`

sync_code(){
    git remote remove old-origin
    git remote rename origin old-origin
    git remote add origin git@49.4.6.199:${group}/${prj_name}.git
    # 首次先推master
    git pull
}



transfer(){

    prj_dir=`realpath ${prj_name}`
    cd ${prj_dir}
	git checkout master
	git remote rename origin old-origin
    git remote add origin git@git.music-z.com:${group}/${prj_name}.git
	# 首次先推master
	git push -u origin --all
	git push -u origin --tags

    all_branch=`git branch -a | grep origin|awk -F 'origin/' '{print $NF}'`
    for branch in ${all_branch}
    do
      echo   ${prj_name} branch  $branch is transing
      sleep 1
	  git checkout ${branch}
      git push -u origin --all
	  git push -u origin --tags
    done
}


if [ "${prj_name}" == "${dir_prj}"  ] 
then 
    echo  "${prj_name}" is transfer
    transfer
else
   echo please check input prj_name,you input prj_name is ${prj_name} 
fi



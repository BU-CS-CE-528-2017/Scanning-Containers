localPATH=`scap-security-guide`                          # path of current dire$
sep='---------------'
loc_directory='scap-security-guide'
git_url='https://github.com/OpenSCAP/'
remote_directory=$git_url$loc_directory

git clone $remote_directory

for d in $loc_directory; do
  echo $sep"Checking Status of" $d$sep
  echo "Pulling remote repo..."
  remoteRepo="https://github.com/OpenSCAP/scap-security-guide.git"    # locatio$
  git -C $d remote add upstream $remoteRepo  # add remote repo as upstream
  git -C $d checkout master
  echo -e "\n"
  git -C $d status            # run git status
  echo -e '\n'
done
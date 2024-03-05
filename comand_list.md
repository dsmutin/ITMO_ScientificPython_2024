# part 1
git clone https://github.com/dsmutin/ITMO_ScientificPython_2024

# part2

## 1
mv *txt ./ITMO_ScientificPython_2024/
cd ./ITMO_ScientificPython_2024/
git branch HW1
git switch HW1

## 2
git add *txt

## 3
git commit -m "task 2.3: add new files"

## 4
git push -u origin HW1

## 5
git branch testing

## 6
echo -e "This is a change." >> hw1.txt

## 7
git commit -a -m "task 2.7: change hw1"
git push origin HW1

## 8
git switch testing
git status testing
echo -e "This is a change." >> test_revert.txt

## 9
git add test_revert.txt
git commit -m "task 2.9: change test_revert.txt"

## 10
git push -u origin testing

## 11
git switch HW1
git commit -a -m "task 2.11: merge"
git merge testing
git push origin HW1
### 3 branches, 
#### HW1 with all changes, 
#### testing without changed 2.7, 
#### main with README.md only

## 12
git revert -m 1 HEAD
git status
git commit -m "task 2.12: revert"
git push origin HW1

## 13
git checkout testing
echo -e "This is a change." >> test_revert_merge.txt

## 14
git add test_revert_merge.txt
git commit -m "task 2.14: change test_revert_merge.txt"
git push origin testing

## 15
git checkout HW1
git merge testing
### All is fine.... 
#### I think that there should be an issue that different files in testing branch and HW1 branch have different changes, so maybe I have a problem in revert command.
#### Why this conflict is avoiding, I don't know...
git push origin HW1

git add command_list.md
git push origin HW1

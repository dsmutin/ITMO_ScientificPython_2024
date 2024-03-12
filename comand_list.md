# part 1
```{bash}
git clone https://github.com/dsmutin/ITMO_ScientificPython_2024
```

# part2

```{bash}
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
```
3 branches, 
- HW1 with all changes, 
- testing without changed 2.7, 
- main with README.md only


```{bash}
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
git push origin HW1
```

Current state: 
HW1/testing: hw1 #7/3; revert #12/9; revert_merge #14/14
File revert in HW1 without changes.
It happends because we revert this changes at stage 12, while changed file stayed only in testing branch.

I thought that it is an expected behavior before initial pull request))

Merge works with the last commits, so if some changes (and revert consider as change) happends, it use the last commited file. To solve this problem, we can revert revert itself, or update file revert in testing branch

```{bash}
## 16
git revert ab53698d61c08a74daf13c49ccfe2314bc777c48
cat test_revert.txt #2 lines

git push origin HW1
```

All merged successfully, so - delete testing branch

```{bash}
git push origin --delete testing
## 17
git push origin HW1

git add command_list.md
git push origin HW1

## 18
Here we are
```

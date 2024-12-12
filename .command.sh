 ./venv/Scripts/activate

# for QAT
git checkout qat ;; git merge dev ;; git add . ;; git commit -m "20241211" ;; git push -u origin qat

# for prod
git checkout prod ;; git merge qat ;; git add . ;; git commit -m "20241211" ;; git push -u origin prod

#  --- 進入SDK
aws s3 ls # 檢查是否在環境
$env:AWS_PROFILE="intern"
 
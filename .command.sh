 ./venv/Scripts/activate


# for dev
git add . ;; git commit -m "modulize 20241216" ;; git push -u origin dev

# for QAT
git checkout qat ;; git merge dev ;; git add . ;; git commit -m "modulize 20241216" ;; git push -u origin qat

# for prod
git checkout prod ;; git merge qat ;; git add . ;; git commit -m "modulize 20241216" ;; git push -u origin prod

#  --- 進入SDK
aws s3 ls # 檢查是否在環境
$env:AWS_PROFILE="intern"
 
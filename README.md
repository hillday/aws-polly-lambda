# aws-polly-lambda
> `main.go` call polly lambda program 

> `nlp_result_to_audio.py` nlp output result convert audio use polly lambda which publish by api gateway

> `s3-mediaconvert-lambda.py` s3 upload object auto trigger mediaconvert

> `invoke_sagemaker_endpoint.py` invoke sagemaker endpoint

# comliper and upload main.go
### complier
```
GOOS=linux GOARCH=amd64 go build -o main main.go
```
### zip
```
zip main.zip main
```
###
upload to lambda
###
create Api Gateway router to lambda

# invoke sagamaker endpoint policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "sagemaker:InvokeEndpoint",
            "Resource": "*"
        }
    ]
}
```
 create policy and attach to execute role

import json
import boto3
import urllib.parse

def get_json_template():
    template = {
      "Queue": "arn:aws:mediaconvert:us-east-1:xxxxx:queues/Default",
      "UserMetadata": {},
      "Role": "arn:aws:iam::xxxxx:role/MediaConvert_Default_Role",
      "Settings": {
        "TimecodeConfig": {
          "Source": "ZEROBASED"
        },
        "OutputGroups": [
          {
            "Name": "File Group",
            "Outputs": [
              {
                "ContainerSettings": {
                  "Container": "MP4",
                  "Mp4Settings": {}
                },
                "VideoDescription": {
                  "Width": 720,
                  "VideoPreprocessors": {
                    "Deinterlacer": {},
                    "NoiseReducer": {
                      "Filter": "TEMPORAL",
                      "TemporalFilterSettings": {
                        "Strength": 4,
                        "Speed": -1
                      }
                    }
                  },
                  "CodecSettings": {
                    "Codec": "H_264",
                    "H264Settings": {
                      "ParNumerator": 1,
                      "NumberReferenceFrames": 3,
                      "GopSize": 3,
                      "GopBReference": "ENABLED",
                      "HrdBufferSize": 4000000,
                      "MaxBitrate": 2000000,
                      "ParDenominator": 1,
                      "SpatialAdaptiveQuantization": "ENABLED",
                      "TemporalAdaptiveQuantization": "ENABLED",
                      "FlickerAdaptiveQuantization": "DISABLED",
                      "RateControlMode": "QVBR",
                      "QvbrSettings": {
                        "QvbrQualityLevel": 7
                      },
                      "CodecProfile": "HIGH",
                      "AdaptiveQuantization": "MEDIUM",
                      "SceneChangeDetect": "TRANSITION_DETECTION",
                      "QualityTuningLevel": "SINGLE_PASS_HQ",
                      "GopSizeUnits": "SECONDS",
                      "ParControl": "SPECIFIED",
                      "NumberBFramesBetweenReferenceFrames": 5
                    }
                  }
                },
                "AudioDescriptions": [
                  {
                    "CodecSettings": {
                      "Codec": "AAC",
                      "AacSettings": {
                        "Bitrate": 96000,
                        "CodingMode": "CODING_MODE_2_0",
                        "SampleRate": 48000
                      }
                    }
                  }
                ],
                "NameModifier": "-aws-2"
              }
            ],
            "OutputGroupSettings": {
              "Type": "FILE_GROUP_SETTINGS",
              "FileGroupSettings": {
                "Destination": "s3://xxxxx/media-convert-output/"
              }
            }
          }
        ],
        "Inputs": [
          {
            "AudioSelectors": {
              "Audio Selector 1": {
                "DefaultSelection": "DEFAULT"
              }
            },
            "VideoSelector": {},
            "TimecodeSource": "ZEROBASED",
            "FileInput": "https://xxxxx/86641804.mp4"
          }
        ]
      },
      "AccelerationSettings": {
        "Mode": "DISABLED"
      },
      "StatusUpdateInterval": "SECONDS_60",
      "Priority": 0
    }
    
    return template

def lambda_handler(event, context):
  
    client = boto3.client('mediaconvert')
    endpoints = client.describe_endpoints()
    
    # print(endpoints)
    mediaconvert_client = boto3.client('mediaconvert', endpoint_url=endpoints['Endpoints'][0]['Url'])

    job_object = get_json_template()
    
    # Get Event bucket and key
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    cv_file = f's3://{bucket}/{key}'
    # Replace key to template
    job_object['Settings']['Inputs'][0]['FileInput'] = cv_file
    print(job_object)
    # Create Convert Job
    response = mediaconvert_client.create_job(**job_object)
    print(response)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

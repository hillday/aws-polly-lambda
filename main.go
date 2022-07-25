package main

import (
        "github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws"
        "github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
        "github.com/aws/aws-sdk-go/service/polly"
	"github.com/aws/aws-lambda-go/events"
	 "context"
   	 "fmt"
    	 "os"
    	 "strings"
    	 "io"
	 "log"
	 "bytes"
	 "encoding/json"
)

type MyEvent struct {
        Text string `json:"text"`
	Name string `json:"name"`
	VoiceId string `json:"voiceId"`
}

func CovText2MediaWithPolly(text string,fileName string,voiceId string) (string, error){
    // Create Polly client
    svc := polly.New(session.New())

    // Output to MP3 using voice Joanna
    input := &polly.SynthesizeSpeechInput{Engine: aws.String("neural"),OutputFormat: aws.String("mp3"), Text: aws.String(text), VoiceId: aws.String(voiceId)}

    output, err := svc.SynthesizeSpeech(input)
    if err != nil {
        fmt.Println("Got error calling SynthesizeSpeech:")
        fmt.Print(err.Error())
        os.Exit(1)
    }
   
    // Save as MP3
    names := strings.Split(fileName, ".")
    name := names[0]
    mp3File := "/tmp/" + name + ".mp3"

    outFile, err := os.Create(mp3File)
    if err != nil {
        fmt.Println("Got error creating " + mp3File + ":")
        fmt.Print(err.Error())
        os.Exit(1)
    }

    defer outFile.Close()
    _, err = io.Copy(outFile, output.AudioStream)
    if err != nil {
        fmt.Println("Got error saving MP3:")
        fmt.Print(err.Error())
        os.Exit(1)
    }
    return mp3File,nil
}

func uploadFile(session *session.Session, uploadFileDir string, name string) error {

    upFile, err := os.Open(uploadFileDir)
    if err != nil {
        return err
    }
    defer upFile.Close()

    upFileInfo, _ := upFile.Stat()
    var fileSize int64 = upFileInfo.Size()
    fileBuffer := make([]byte, fileSize)
    upFile.Read(fileBuffer)

    _, err = s3.New(session).PutObject(&s3.PutObjectInput{
        Bucket:               aws.String("xxxx"),//修改存储桶名称
        Key:                  aws.String("audio/" + name),
        ACL:                  aws.String("private"),
        Body:                 bytes.NewReader(fileBuffer),
        ContentLength:        aws.Int64(fileSize),
        ContentType:          aws.String("audio/mp3"),
        ContentDisposition:   aws.String("attachment"),
        ServerSideEncryption: aws.String("AES256"),
    })
    return err
}

func HandleRequest(ctx context.Context, event MyEvent) (string, error) {
	mp3File,err := CovText2MediaWithPolly(event.Text,event.Name,event.VoiceId)
	if err != nil {
		return fmt.Sprintf("0 Convert text %s error",event.Text),nil
	}
        
	// Upload Files
    	err = uploadFile(session.New(), mp3File, event.Name)
    	if err != nil {
        	log.Fatal(err)
    	}
        return fmt.Sprintf("3 Convert text %s success", event.Text), nil
}

func handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	var event MyEvent
	json.Unmarshal([]byte(request.Body), &event)

	mp3File,err := CovText2MediaWithPolly(event.Text,event.Name,event.VoiceId)
        if err != nil {
        	log.Fatal(err)
	}

        // Upload Files
        err = uploadFile(session.New(), mp3File, event.Name)
        if err != nil {
                log.Fatal(err)
        }

	return events.APIGatewayProxyResponse{Body: "success", StatusCode: 200}, nil
}

func main() {
        lambda.Start(handler)
}

READ ME


In Progress........

   ###    ##      ##  ######     ######## ########     ###    ##    ##  ######   ######   #######  ##     ## ########
  ## ##   ##  ##  ## ##    ##       ##    ##     ##   ## ##   ###   ## ##    ## ##    ## ##     ## ###   ### ##     ##
 ##   ##  ##  ##  ## ##             ##    ##     ##  ##   ##  ####  ## ##       ##       ##     ## #### #### ##     ##
##     ## ##  ##  ##  ######        ##    ########  ##     ## ## ## ##  ######  ##       ##     ## ## ### ## ########
######### ##  ##  ##       ##       ##    ##   ##   ######### ##  ####       ## ##       ##     ## ##     ## ##
##     ## ##  ##  ## ##    ##       ##    ##    ##  ##     ## ##   ### ##    ## ##    ## ##     ## ##     ## ##
##     ##  ###  ###   ######        ##    ##     ## ##     ## ##    ##  ######   ######   #######  ##     ## ##git a

This project will initiate a step function off an s3 PUT object audio file. It will then transcribe the audio to text
using AWS Transcribe. Those Json documents will then me be dumped into an s3 bucket of choice. That will trigger a
lambda that will send the text data to AWS comprehend and return Sentiment Analysis and Key Phrase Data.


Comprehend data will be sent to a glue data base , or elastic search, where this data can be interpereted as needed. (i.
 graphs, pie-charts)


 In the end ultimately all you will need to do is deploy a cloud formation in your AWS Console.
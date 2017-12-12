from __future__ import print_function
import json
import os
from watson_developer_cloud import ConversationV1

#########################
# message
#########################

conversation = ConversationV1(
    username='8e658476-e309-4853-a05b-874da398fc92',
    password='wYr0UtJik3AM',
    version='2017-04-21',
    url='https://gateway.watsonplatform.net/conversation/api/v1')

# replace with your own workspace_id
workspace_id = 'fd6bb0f5-edcc-41de-b8eb-8463befac5e0'
if os.getenv("conversation_workspace_id") is not None:
    workspace_id = os.getenv("conversation_workspace_id")


# recognize user image and set context to the chatbot
context = {
  wearingPant: 1,
  wearingTeeshirt: 1,
  wearingSkirt: 0,
  wearingJacket: 1,
  wearingBlouse: 0
}

print("입고계신 옷을 분석 중이에요. 패션도우미 챗봇과 대화를 시작하세요!")

while true:
  line = readline(">> ")
  response = conversation.message(workspace_id=workspace_id, input={
    'text': line, context: context})
  print(response.text)

  if response.context["finalized"]:
    break

  if (response.context["proposal"]):
    # choose an image and display to the user
    displayImage(response.context)

print("패션도우미 챗봇이었습니다. 즐거운 쇼핑 되세요~")
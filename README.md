"# RESTful API Linebot" 

•**commit #1 initial a project skeleton**
  •This is an Line-message-api with flask , please install required python packages Documentation  
  •init flask app with python
![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/56edd7d7-fc22-41b1-9cd8-e0f29b86e3ae)


• **commit #2 setup necessary configuration of LINE and MongoDB**
  • create new channek for message api
![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/5d20d5af-5f02-4033-b4a4-220f6e8102b9)
  • create new collection in mongodb 
![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/c92f07f6-4e85-46ad-a993-296bb58bcb0e)


• **commit #3 connect and access MongoDB** 
  • Create objects for MongoDB/collection connection 
![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/a50a66fc-011c-4837-aab0-eab35745ca36)
  •Create model/DTO objects to save/query user messages with MongoDB  
![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/6ec166cc-3278-4753-b5e1-c16a78a6ffd4)


• **commit #4 receive and store the message**
  •Create RESTful API for receiving messages from Line webhook, save the user info and message in MongoDB 
  ![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/7f237e16-5458-4e90-9f5e-5f668faf7960)
  •(hint: using ngrok for local test to generate an HTTPS endpoint)
  ![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/5fe6663e-6796-4777-a4ee-ba91268beefa)


• **commit #5 send message to LINE** 
  •Create an API for sending message to LINE 
![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/8159579a-9718-4304-8071-b293c21f5df4)


• **commit #6 query message from MongoDB** 
  •Create an API query message list of the user from MongoDB 
  ![image](https://github.com/YiChe0703/RESTful-API-Linebot/assets/80759343/bb4bd8c5-7a6c-4039-8916-8fb050d01dbe)

• Provide a demo video of test(postman) under repository demo.mp4

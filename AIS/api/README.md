#人脸检测接口
curl -X POST "127.0.0.1:8888/face_detect" -F "image=this is a test" -F "company_id=useease"
字段 image base64
    company_id string
#Todo api_key
#Todo secert_key 

#人脸上传接口，抽取特征
curl -X POST "127.0.0.1:8888/add_face" -F "face=this is a test" -F "name=kenwood" -F "company=useease" -F "worker_id=12"
字段：   face，base64，图片
        name，string，名字
        company，string，公司名
        worker_id，int,工号
   




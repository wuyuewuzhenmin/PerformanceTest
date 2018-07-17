#encoding: utf-8
import json

str = '{"accessToken": "521", "User-Agent": "1)"}'

data ={
    "gmt": "28800",
	"text": "人生若只如初见，何事秋风悲画扇。等闲变却故人心，却道故人心易变。骊山语罢清宵半，泪雨零铃终不怨。"
        }

print type(data)


# j = json.loads(data)
j = json.dumps(data)

print(j)
print(type(j))
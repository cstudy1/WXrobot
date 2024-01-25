import pandas as pd
import numpy as np
from uiautomation import WindowControl,MenuControl
import time
import difflib
from openai import OpenAI
from dotenv import load_dotenv
import os
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

load_dotenv()




def calculate_similarity(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).ratio()




def chatgpt(question):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("api-key"),
        max_retries=5,
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model="gpt-3.5-turbo",
        )
        print(chat_completion['choices'][0]['message']['content'])
        return chat_completion['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry I can't anwser"
    





wx = WindowControl(
    Name ='微信',
    waitTime=2,
)
print(wx)
# 切换窗口
wx.SwitchToThisWindow(waitTime=2)

hw = wx.ListControl(Name='会话')
print("寻找会话控件绑定",hw)
df = pd.read_csv("回复数据.csv",encoding='GBK')
#死循环接受消息
while True:
    # 查找未读消息
    we = hw.TextControl(searchDepth=4)
    print("we.name:   "+str(we.Name))

    # 维持死循环
    while not we.Exists(0):
        pass

    if we.Name:
        # 点击未读消息
        time.sleep(5)
        we.Click(simulateMove=False)

        last_msg = wx.ListControl(Name="消息").GetChildren()[-1].Name
        print('读取最后一条消息',last_msg)

        # 提取返回消息
        # 计算每个关键词与 last_msg 的相似性
        similarities = df['关键词'].apply(lambda keyword: calculate_similarity(keyword, last_msg))

        # 找到相似性最高的关键词的索引
        best_match_index = similarities.idxmax()

        # 获取对应的回复内容
        best_reply = df.at[best_match_index, '回复内容']

        print("Best matching keyword:", df.at[best_match_index, '关键词'])
        print("Best matching reply:", best_reply)

        # best_reply.dropna(axis=0, how='any',inplace=True)
        # ar = np.array(best_reply).tolist()
        ar=None
        #匹配到内容时
        if ar:
            time.sleep(3)

            wx.SendKeys(ar, waitTime=2)

            # 第二步：发送消息
            wx.SendKeys('{Enter}', waitTime=2)
            
            # 通过消息匹配检索会话栏的联系人
            hw.TextControl(SubName="文件传输助手").RightClick()

        else:
            time.sleep(3)
            
            wx.SendKeys("Searching......",waitTime=2)

            wx.SendKeys('{Enter}', waitTime=2)
            
            last_msg="请用中文回答："+last_msg

            anwser = chatgpt(last_msg)

            wx.SendKeys(anwser,waitTime=2)

            wx.SendKeys('{Enter}', waitTime=2)



            # 通过消息匹配检索会话栏的联系人
            hw.TextControl(SubName="文件传输助手").RightClick()


            













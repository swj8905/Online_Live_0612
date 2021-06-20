import streamlit as st

st.text("스트림릿 예제 입니다.")
st.text("테스트 중입니다.")
st.text("text함수는 한줄 씩 기록하게 해줍니다.")

st.write("---")
st.write("write 함수 테스트 중입니다.")
st.write("# 샾 기호를 넣으면 이렇게 됩니다.")
st.write("## 샾 기호 2개를 넣으면 이렇게 됩니다.")
st.write("### 샾 기호 3개를 넣으면 이렇게 됩니다.")
st.write("#### 샾 기호 4개를 넣으면 이렇게 됩니다.")
st.write("##### 샾 기호 5개를 넣으면 이렇게 됩니다.")
st.write("###### 샾 기호 6개를 넣으면 이렇게 됩니다.")
st.write("> 이런 것도 됩니다.")
st.write(">> 이런 것도 됩니다.")
st.write(">>> 이런 것도 됩니다.")
st.write("https://www.naver.com")
a = {"짜장면":5000, "짬뽕":5000, "탕수육":10000}
st.write(a)
st.code("print('hello world')")
st.write("-----------------------")

"""
# 매직 커맨드

굳이 write()함수를 쓰지 않아도 됩니다.

----

> 표를 띄우고 싶으면, 그냥 코드에 표를 그리면 됩니다.

|        |  수학       |  평가      |
|--------|-------------|:------------:|
| 철수   | 90          | 잘했어요.  |
| 영희   | 60          | 분발하세요.|

https://www.naver.com

```python
print("Hello World")
```

"""

import webbrowser
if st.button("네이버"):
    webbrowser.open("https://www.naver.com")











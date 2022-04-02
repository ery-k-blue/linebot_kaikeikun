# 会計君

## 会計君って？
旅行や遊びに行ったとき、こういったことはないでしょうか？
![image](https://user-images.githubusercontent.com/54242557/161373614-8d25054c-3d63-4074-af23-b3ae3c811e10.png)

「これ誰が払ったんだっけ？」「ここの会計分計算に入ってなくない？」「AさんがBさんに2000円支払って、、、」「私もっと払ったよね？もらう金額少なくない？？？」

そうなんです、旅行の後の精算は非常に計算がめんどくさい！！
せっかくの楽しかった旅行が精算で揉めて友情に傷が入ることもあります（ないです）

そういう時に使えるのが、今回作成した「会計君」！！！
使い方は簡単、旅行行くときLINEグループ作りますよね？？
そのLINEグループに会計君botを追加して、支払いが発生したときにグループに金額を打ち込むだけ！！

これでどこに遊びに行くときでも安心です！

## 使い方
会計君はグループに追加して、使用します。
トーク内容は、保存されることはありません。（※金額を入力した際の金額情報は保存されます。）

![image](https://user-images.githubusercontent.com/54242557/158563413-1e491b72-a751-4d86-861b-925455114956.png)


### メニューを呼び出す
- 会計君がグループに存在する状態で、「会計君」とメッセージを送信するとメニューが送信されます。

![image](https://user-images.githubusercontent.com/54242557/158563517-df46d575-e774-4e2f-b346-ab5ddce8c60d.png)

### 支払情報を入力する
支払情報の入力方法は「支払った本人が入力する方法」と「他の人が代理で入力する方法」の2つ存在します。
※いずれも、支払った金額のみを入力することで、会計君が反応します。

#### 支払った本人が入力する方法
支払った本人が入力する際は、「支払った金額」のみを入力します。
![image](https://user-images.githubusercontent.com/54242557/158563670-da823ac4-4f49-4b7d-a2ed-e96bf78236fe.png)

その他の入力は、無視されます。
```
ダメな入力例
500円
○○が500円払った
```

#### 他の人が代理で入力する方法
他の人が代理で入力する際は、「<支払った人メンション>＋支払った金額」を入力します。

![image](https://user-images.githubusercontent.com/54242557/158563768-d23ccf5a-ded0-4ce2-9ba5-b6f928fd0385.png)

### 会計を行う
- 会計を行いたい場合は、メニューの「会計を行う」ボタンを押します。（ボタンを押すと「会計を行う」が自動で送信されます。）
- 次に、割り勘を行うメンバーをメンションで選択します。（入力者は自動で含まれます。）
- すると、誰が誰に何円払えばよいかの情報が送信されます。

![image](https://user-images.githubusercontent.com/54242557/158563853-252b7e31-05cd-4ac3-a730-7d9986d2f469.png)
